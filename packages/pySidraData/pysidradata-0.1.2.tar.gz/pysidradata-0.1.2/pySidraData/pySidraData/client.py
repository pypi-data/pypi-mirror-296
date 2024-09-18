import logging
import random
from typing import List, Dict, Any, Optional, Union

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from sidrapy import get_table

from .models import RootData, Research, Aggregate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Client:
    BASE_URL = "https://servicodados.ibge.gov.br/api/v3/agregados"

    def __init__(self):
        self._root_data = None
        self._metadata_cache: Dict[str, Dict[str, Any]] = {}
        self.session = self._create_session()

    @staticmethod
    def _create_session() -> requests.Session:
        """Create a session with retry strategy."""
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        return session

    def _fetch_root_data(self) -> RootData:
        """Fetch the root data from the API and convert it to a structured Python object."""
        try:
            response = self.session.get(self.BASE_URL)
            response.raise_for_status()
            data = response.json()

            researches = []
            for item in data:
                agregados = [
                    Aggregate(id=str(agg["id"]), nome=agg["nome"])
                    for agg in item.get("agregados", [])
                ]
                research = Research(
                    id=str(item["id"]), nome=item["nome"], agregados=agregados
                )
                researches.append(research)

            return RootData(research_list=researches)
        except requests.RequestException as e:
            logger.error(f"Error fetching root data: {e}")
            raise

    def get_root_data(self) -> RootData:
        """Retrieve or fetch the root data."""
        if self._root_data is None:
            self._root_data = self._fetch_root_data()
        return self._root_data

    def get_metadata(self, aggregate_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Fetch metadata for a specific aggregate ID.
        If no ID is provided, fetch a random one.
        """
        all_aggregate_ids = self.list_all_aggregate_ids()

        if aggregate_id is None:
            aggregate_id = random.choice(all_aggregate_ids)
        elif str(aggregate_id) not in all_aggregate_ids:
            raise ValueError(f"Invalid aggregate ID. Choose from: {all_aggregate_ids}")

        if aggregate_id in self._metadata_cache:
            return self._metadata_cache[aggregate_id]

        try:
            response = self.session.get(f"{self.BASE_URL}/{aggregate_id}/metadados")
            response.raise_for_status()
            data = response.json()
            self._metadata_cache[aggregate_id] = data
            return data
        except requests.RequestException as e:
            logger.error(
                f"Error fetching metadata for aggregate ID {aggregate_id}: {e}"
            )
            raise

    def get_root_data_as_dataframe(self) -> pd.DataFrame:
        """Convert the root data to a Pandas DataFrame."""
        root_data = self.get_root_data()
        records = [
            {
                "research_id": research.id,
                "research_name": research.nome,
                "aggregate_id": aggregate.id,
                "aggregate_name": aggregate.nome,
            }
            for research in root_data.research_list
            for aggregate in research.agregados
        ]
        return pd.DataFrame(records)

    def list_all_aggregate_ids(self) -> List[str]:
        """List all available aggregate IDs."""
        root_data = self.get_root_data()
        return [
            str(aggregate.id)
            for research in root_data.research_list
            for aggregate in research.agregados
        ]

    def list_available_variables(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all variables available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        return [
            variable.get("nome", "Unknown")
            for variable in metadata.get("variaveis", [])
        ]

    def list_available_periods(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all periods available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        periods = metadata.get("periodosDisponiveis", [])
        return [period.get("id", "Unknown") for period in periods]

    def list_available_classifications(
        self, aggregate_id: Optional[str] = None
    ) -> List[str]:
        """List all classifications available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        return [
            classification.get("nome", "Unknown")
            for classification in metadata.get("classificacoes", [])
        ]

    def get_data(
        self,
        table_code: str,
        territorial_level: str = "1",
        ibge_territorial_code: Union[str, List[str]] = "all",
        period: Union[str, List[str]] = "last",
        **kwargs,
    ) -> pd.DataFrame:
        """
        Fetch data from a SIDRA table with customizable parameters.

        :param table_code: The code of the table to fetch. (Required)
        :param territorial_level: The territorial level to consider. Default is '1'.
        :param ibge_territorial_code: The IBGE territorial code(s). Default is 'all'.
        :param period: The period(s) to consider. Default is 'last'.
        :param kwargs: Additional keyword arguments to pass to sidrapy.get_table.
        :return: A pandas DataFrame containing the requested data.
        """
        if not table_code:
            raise ValueError("The 'table_code' parameter is required.")

        # Ensure required arguments are provided
        params = {
            "table_code": table_code,
            "territorial_level": territorial_level,
            "ibge_territorial_code": ibge_territorial_code,
            "period": period,
        }

        # Update params with any additional kwargs
        params.update(kwargs)

        try:
            data = get_table(**params)
            return data
        except Exception as e:
            logger.error(f"Error fetching data with parameters {params}: {e}")
            raise

    def get_data_preview(
        self,
        table_code: str,
        limit: int = 5,
        territorial_level: str = "1",
        ibge_territorial_code: Union[str, List[str]] = "all",
        period: Union[str, List[str]] = "last",
        **kwargs,
    ) -> pd.DataFrame:
        """
        Fetch a small preview of data from a SIDRA table.

        :param table_code: The code of the table to fetch. (Required)
        :param limit: Number of rows to return in the preview.
        :param territorial_level: The territorial level to consider. Default is '1'.
        :param ibge_territorial_code: The IBGE territorial code(s). Default is 'all'.
        :param period: The period(s) to consider. Default is 'last'.
        :param kwargs: Additional keyword arguments for sidrapy.get_table.
        :return: A pandas DataFrame containing the data preview.
        """
        data = self.get_data(
            table_code=table_code,
            territorial_level=territorial_level,
            ibge_territorial_code=ibge_territorial_code,
            period=period,
            **kwargs,
        )
        return data.head(limit)

    def list_geographical_levels(self, aggregate_id: Optional[str] = None) -> List[str]:
        """List all geographical levels available for a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        return list(metadata.get("nivelTerritorial", {}).keys())

    def list_territorial_levels(
        self, aggregate_id: Optional[str] = None, territorial_type: Optional[str] = None
    ) -> Union[List[str], Dict[str, List[str]]]:
        """
        List territorial levels for a specific type in a given aggregate ID.
        If no type is provided, return all levels.
        """
        metadata = self.get_metadata(aggregate_id)
        levels = metadata.get("nivelTerritorial", {})
        if territorial_type:
            return levels.get(territorial_type, [])
        else:
            return levels

    def get_table_description(self, aggregate_id: Optional[str] = None) -> str:
        """Get a detailed description of a specific aggregate ID."""
        metadata = self.get_metadata(aggregate_id)
        return metadata.get("descricao", "No description available.")

    def get_data_summary(
        self,
        table_code: str,
        territorial_level: str = "1",
        ibge_territorial_code: Union[str, List[str]] = "all",
        period: Union[str, List[str]] = "last",
        **kwargs,
    ) -> pd.DataFrame:
        """
        Retrieve a statistical summary of the data.

        :param table_code: The code of the table to fetch. (Required)
        :param territorial_level: The territorial level to consider. Default is '1'.
        :param ibge_territorial_code: The IBGE territorial code(s). Default is 'all'.
        :param period: The period(s) to consider. Default is 'last'.
        :param kwargs: Additional keyword arguments to pass to sidrapy.get_table.
        :return: A pandas DataFrame containing the data summary.
        """
        data = self.get_data(
            table_code=table_code,
            territorial_level=territorial_level,
            ibge_territorial_code=ibge_territorial_code,
            period=period,
            **kwargs,
        )
        return data.describe()

    def list_all_tables(self) -> List[Dict[str, str]]:
        """List all available tables in SIDRA."""
        root_data = self.get_root_data()
        return [
            {"id": aggregate.id, "name": aggregate.nome}
            for research in root_data.research_list
            for aggregate in research.agregados
        ]

    def __repr__(self):
        return f"<Client with {len(self)} research items>"

    def __len__(self):
        """Return the number of research items."""
        return len(self.get_root_data().research_list)

    def __getitem__(self, index):
        """Get a research item by index."""
        return self.get_root_data().research_list[index]

    def __iter__(self):
        """Return an iterator over the research items."""
        return iter(self.get_root_data().research_list)
