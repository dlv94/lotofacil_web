import random
from typing import Dict, List, Set, Tuple

from game_config import GameConfig
from generated_game import GeneratedGame
from quadrant_set import QuadrantSet


import secrets
import random
from typing import List, Set, Tuple, Dict

class GameGenerator:
    """
    Responsável pela geração dos jogos da Lotofácil
    respeitando os números fixos e a distribuição
    definida em cada conjunto de quadrantes.
    """

    NUMBERS_PER_GAME = 15

    QUADRANTS = {
        1: list(range(1, 6)),
        2: list(range(6, 11)),
        3: list(range(11, 16)),
        4: list(range(16, 21)),
        5: list(range(21, 26))
    }

    # =========================================================
    # MÉTODO PRINCIPAL
    # =========================================================

    def generate(
        self,
        config: GameConfig
    ) -> List[GeneratedGame]:

        generated_games = []
        global_combinations: Set[Tuple[int, ...]] = set()

        for quadrant_set in config.quadrant_sets:

            games_from_set = self._generate_set_games(
                fixed_numbers=config.fixed_numbers,
                quadrant_set=quadrant_set,
                global_combinations=global_combinations
            )

            generated_games.extend(
                games_from_set
            )

        return generated_games

    # =========================================================
    # GERAÇÃO DE UM CONJUNTO
    # =========================================================

    def _generate_set_games(
        self,
        fixed_numbers: List[int],
        quadrant_set: QuadrantSet,
        global_combinations: Set[Tuple[int, ...]]
    ) -> List[GeneratedGame]:
        """
        Gera a quantidade de jogos definida para
        um conjunto específico, garantindo unicidade global.
        """

        games = []

        while (
            len(games)
            < quadrant_set.number_of_games
        ):

            numbers = self._generate_single_game(
                fixed_numbers=fixed_numbers,
                quadrant_set=quadrant_set
            )

            game_key = tuple(
                sorted(numbers)
            )

            # Evita jogos repetidos tanto no conjunto quanto globalmente.
            if game_key in global_combinations:
                continue

            global_combinations.add(
                game_key
            )

            games.append(
                GeneratedGame(
                    set_id=quadrant_set.set_id,
                    game_number=len(games) + 1,
                    quadrant_distribution=[
                        quadrant_set.quadrant_distribution[1],
                        quadrant_set.quadrant_distribution[2],
                        quadrant_set.quadrant_distribution[3],
                        quadrant_set.quadrant_distribution[4],
                        quadrant_set.quadrant_distribution[5],
                    ],
                    numbers=sorted(numbers)
                )
            )

        return games

    # =========================================================
    # GERAÇÃO DE UM JOGO
    # =========================================================

    def _generate_single_game(
        self,
        fixed_numbers: List[int],
        quadrant_set: QuadrantSet
    ) -> List[int]:
        """
        Gera um único jogo respeitando a quantidade
        configurada para cada quadrante.
        """

        selected_numbers = set(
            fixed_numbers
        )

        fixed_by_quadrant = (
            self._group_fixed_numbers_by_quadrant(
                fixed_numbers
            )
        )

        for quadrant in range(1, 6):

            configured_quantity = (
                quadrant_set
                .quadrant_distribution[
                    quadrant
                ]
            )

            fixed_numbers_in_quadrant = (
                fixed_by_quadrant[
                    quadrant
                ]
            )

            random_quantity = (
                configured_quantity
                - len(
                    fixed_numbers_in_quadrant
                )
            )

            if random_quantity <= 0:
                continue

            available_numbers = [
                number
                for number in self.QUADRANTS[
                    quadrant
                ]
                if number not in selected_numbers
            ]

            selected_numbers.update(
                self._select_random_numbers(
                    available_numbers,
                    random_quantity
                )
            )

        return list(
            selected_numbers
        )

    # =========================================================
    # AGRUPAMENTO DOS FIXOS
    # =========================================================

    def _group_fixed_numbers_by_quadrant(
        self,
        fixed_numbers: List[int]
    ) -> Dict[int, List[int]]:
        """
        Agrupa os números fixos de acordo com
        o quadrante ao qual pertencem.
        """

        fixed_by_quadrant = {
            quadrant: []
            for quadrant in range(1, 6)
        }

        for number in fixed_numbers:

            quadrant = self._get_quadrant(
                number
            )

            fixed_by_quadrant[
                quadrant
            ].append(
                number
            )

        return fixed_by_quadrant

    # =========================================================
    # IDENTIFICAÇÃO DO QUADRANTE
    # =========================================================

    @staticmethod
    def _get_quadrant(
        number: int
    ) -> int:

        return (
            (number - 1) // 5
        ) + 1

    # =========================================================
    # SELEÇÃO ALEATÓRIA SEGURA
    # =========================================================

    def _select_random_numbers(
        self,
        available_numbers: List[int],
        quantity: int
    ) -> List[int]:
        """
        Seleciona números utilizando o gerador seguro baseado na
        entropia do Sistema Operacional (Secrets).
        """

        if quantity <= 0 or not available_numbers:
            return []

        sample_size = min(quantity, len(available_numbers))

        return secrets.SystemRandom().sample(available_numbers, sample_size)