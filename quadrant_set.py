from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class QuadrantSet:
    """
    Representa uma configuração de distribuição
    dos 15 números entre os 5 quadrantes.
    """

    set_id: int

    number_of_games: int

    quadrant_distribution: Dict[int, int]