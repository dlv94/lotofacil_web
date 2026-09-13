from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class GeneratedGame:
    """
    Representa um jogo gerado a partir de
    um conjunto de quadrantes.
    """

    set_id: int
    game_number: int
    quadrant_distribution: List[int]
    numbers: List[int]