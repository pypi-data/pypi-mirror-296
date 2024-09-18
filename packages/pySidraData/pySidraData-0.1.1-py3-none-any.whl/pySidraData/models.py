from dataclasses import dataclass, field
from typing import List


@dataclass
class Aggregate:
    id: str
    nome: str


@dataclass
class Research:
    id: str
    nome: str
    agregados: List[Aggregate] = field(default_factory=list)


@dataclass
class RootData:
    research_list: List[Research]
