from dataclasses import dataclass, field
from typing import List

from quadrant_set import QuadrantSet


@dataclass(frozen=True)
class GameConfig:
    """
    Representa a configuração completa para
    geração dos jogos da Lotofácil.
    """

    fixed_numbers: List[int] = field(
        default_factory=list
    )

    quadrant_sets: List[QuadrantSet] = field(
        default_factory=list
    )