import unittest
from pySidraData.client import Client


class TestClient(unittest.TestCase):

    def setUp(self):
        """Set up the Client instance for testing."""
        self.client = Client()

    def test_get_root_data(self):
        """Test fetching root data."""
        root_data = self.client.get_root_data()
        self.assertIsNotNone(root_data)
        self.assertTrue(len(root_data.research_list) > 0)

    def test_list_all_aggregate_ids(self):
        """Test listing all aggregate IDs."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        self.assertIsInstance(aggregate_ids, list)
        self.assertTrue(len(aggregate_ids) > 0)

    def test_get_metadata_random(self):
        """Test getting metadata for a random aggregate ID."""
        metadata = self.client.get_metadata()
        self.assertIsNotNone(metadata)
        self.assertIsInstance(metadata, dict)

    def test_get_metadata_specific(self):
        """Test getting metadata for a specific aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            metadata = self.client.get_metadata(aggregate_id)
            self.assertIsNotNone(metadata)
            self.assertIsInstance(metadata, dict)

    def test_get_root_data_as_dataframe(self):
        """Test converting root data to a DataFrame."""
        df = self.client.get_root_data_as_dataframe()
        self.assertFalse(df.empty)

    def test_list_available_variables(self):
        """Test listing available variables for an aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            variables = self.client.list_available_variables(aggregate_id)
            self.assertIsInstance(variables, list)
            self.assertTrue(len(variables) > 0)

    def test_list_available_periods(self):
        """Test listing available periods for an aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            periods = self.client.list_available_periods(aggregate_id)
            self.assertIsInstance(periods, list)
            self.assertTrue(len(periods) > 0)

    def test_search_tables(self):
        """Test searching for tables with a keyword."""
        search_results = self.client.search_tables("population")
        self.assertIsInstance(search_results, list)
        self.assertTrue(len(search_results) > 0)

    def test_list_available_classifications(self):
        """Test listing classifications for an aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            classifications = self.client.list_available_classifications(aggregate_id)
            self.assertIsInstance(classifications, list)
            self.assertTrue(len(classifications) > 0)

    def test_get_data_preview(self):
        """Test fetching a data preview from a SIDRA table."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            data_preview = self.client.get_data_preview(
                table_code=aggregate_id, limit=5
            )
            self.assertFalse(data_preview.empty)

    def test_list_geographical_levels(self):
        """Test listing geographical levels for an aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            geo_levels = self.client.list_geographical_levels(aggregate_id)
            self.assertIsInstance(geo_levels, list)
            self.assertTrue(len(geo_levels) > 0)

    def test_get_table_description(self):
        """Test getting a table description for an aggregate ID."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            description = self.client.get_table_description(aggregate_id)
            self.assertIsInstance(description, str)
            self.assertTrue(len(description) > 0)

    def test_get_data_summary(self):
        """Test fetching a data summary from a SIDRA table."""
        aggregate_ids = self.client.list_all_aggregate_ids()
        if aggregate_ids:
            aggregate_id = aggregate_ids[0]
            data_summary = self.client.get_data_summary(
                table_code=aggregate_id, territorial_level="1", period="last"
            )
            self.assertFalse(data_summary.empty)

    def test_list_all_tables(self):
        """Test listing all available tables in SIDRA."""
        all_tables = self.client.list_all_tables()
        self.assertIsInstance(all_tables, list)
        self.assertTrue(len(all_tables) > 0)


if __name__ == "__main__":
    unittest.main()
