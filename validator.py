from collections import Counter
from typing import Dict

from game_config import GameConfig
from quadrant_set import QuadrantSet


class GameValidator:
    """
    Responsável por validar as regras de negócio
    da configuração dos jogos.
    """

    MIN_NUMBER = 1
    MAX_NUMBER = 25

    NUMBERS_PER_GAME = 15

    QUADRANT_SIZE = 5

    QUADRANTS = (
        1,
        2,
        3,
        4,
        5
    )

    # =========================================================
    # VALIDAÇÃO PRINCIPAL
    # =========================================================

    def validate(
        self,
        config: GameConfig
    ) -> None:

        self._validate_fixed_numbers(
            config.fixed_numbers
        )

        self._validate_quadrant_sets(
            config.quadrant_sets,
            config.fixed_numbers
        )

    # =========================================================
    # NÚMEROS FIXOS
    # =========================================================

    def _validate_fixed_numbers(
        self,
        fixed_numbers: list[int]
    ) -> None:

        if len(fixed_numbers) > self.NUMBERS_PER_GAME:

            raise ValueError(
                f"Um jogo pode possuir no máximo "
                f"{self.NUMBERS_PER_GAME} números fixos."
            )

        duplicates = [
            number
            for number, count in Counter(
                fixed_numbers
            ).items()
            if count > 1
        ]

        if duplicates:

            formatted_numbers = ", ".join(
                str(number)
                for number in sorted(
                    duplicates
                )
            )

            raise ValueError(
                "Existem números fixos repetidos: "
                f"{formatted_numbers}."
            )

        invalid_numbers = [
            number
            for number in fixed_numbers
            if (
                number < self.MIN_NUMBER
                or number > self.MAX_NUMBER
            )
        ]

        if invalid_numbers:

            formatted_numbers = ", ".join(
                str(number)
                for number in sorted(
                    invalid_numbers
                )
            )

            raise ValueError(
                f"Os números fixos devem estar entre "
                f"{self.MIN_NUMBER} e {self.MAX_NUMBER}. "
                f"Inválidos: {formatted_numbers}."
            )

    # =========================================================
    # CONJUNTOS
    # =========================================================

    def _validate_quadrant_sets(
        self,
        quadrant_sets: list[QuadrantSet],
        fixed_numbers: list[int]
    ) -> None:

        if not quadrant_sets:

            raise ValueError(
                "Adicione pelo menos um conjunto "
                "de quadrantes."
            )

        set_ids = [
            quadrant_set.set_id
            for quadrant_set in quadrant_sets
        ]

        duplicated_ids = [
            set_id
            for set_id, count in Counter(
                set_ids
            ).items()
            if count > 1
        ]

        if duplicated_ids:

            formatted_ids = ", ".join(
                str(set_id)
                for set_id in sorted(
                    duplicated_ids
                )
            )

            raise ValueError(
                "Existem identificadores de conjuntos "
                f"repetidos: {formatted_ids}."
            )

        for quadrant_set in quadrant_sets:
             self._validate_quadrant_set(
            quadrant_set,
            fixed_numbers
        )

    # =========================================================
    # CONJUNTO INDIVIDUAL
    # =========================================================

    def _validate_quadrant_set(
        self,
        quadrant_set: QuadrantSet,
        fixed_numbers: list[int]
    ) -> None:

        self._validate_set_id(
            quadrant_set.set_id
        )

        self._validate_number_of_games(
            quadrant_set
        )

        self._validate_distribution(
            quadrant_set
        )

        self._validate_fixed_numbers_distribution(
            quadrant_set,
            fixed_numbers
        )

    # =========================================================
    # ID DO CONJUNTO
    # =========================================================

    @staticmethod
    def _validate_set_id(
        set_id: int
    ) -> None:

        if not isinstance(
            set_id,
            int
        ) or isinstance(
            set_id,
            bool
        ):

            raise ValueError(
                "O identificador do conjunto "
                "deve ser um número inteiro."
            )

        if set_id <= 0:

            raise ValueError(
                "O identificador do conjunto "
                "deve ser maior que zero."
            )

    # =========================================================
    # QUANTIDADE DE JOGOS
    # =========================================================

    @staticmethod
    def _validate_number_of_games(
        quadrant_set: QuadrantSet
    ) -> None:

        number_of_games = (
            quadrant_set.number_of_games
        )

        if not isinstance(
            number_of_games,
            int
        ) or isinstance(
            number_of_games,
            bool
        ):

            raise ValueError(
                f"A quantidade de jogos do conjunto "
                f"{quadrant_set.set_id} deve ser "
                "um número inteiro."
            )

        if number_of_games <= 0:

            raise ValueError(
                f"A quantidade de jogos do conjunto "
                f"{quadrant_set.set_id} deve ser "
                "maior que zero."
            )

    # =========================================================
    # DISTRIBUIÇÃO
    # =========================================================

    def _validate_distribution(
        self,
        quadrant_set: QuadrantSet
    ) -> None:

        distribution = (
            quadrant_set.quadrant_distribution
        )

        if set(
            distribution.keys()
        ) != set(
            self.QUADRANTS
        ):

            raise ValueError(
                f"O conjunto {quadrant_set.set_id} "
                "deve possuir exatamente os "
                "quadrantes Q1, Q2, Q3, Q4 e Q5."
            )

        for quadrant, quantity in (
            distribution.items()
        ):

            if not isinstance(
                quantity,
                int
            ) or isinstance(
                quantity,
                bool
            ):

                raise ValueError(
                    f"O valor do Q{quadrant} "
                    f"do conjunto {quadrant_set.set_id} "
                    "deve ser um número inteiro."
                )

            if quantity < 0:

                raise ValueError(
                    f"O valor do Q{quadrant} "
                    f"do conjunto {quadrant_set.set_id} "
                    "não pode ser negativo."
                )

            if quantity > self.QUADRANT_SIZE:

                raise ValueError(
                    f"O Q{quadrant} do conjunto "
                    f"{quadrant_set.set_id} não pode "
                    f"possuir mais de "
                    f"{self.QUADRANT_SIZE} números."
                )

        total = sum(
            distribution.values()
        )

        if total != self.NUMBERS_PER_GAME:

            raise ValueError(
                f"O conjunto {quadrant_set.set_id} "
                f"possui {total} números. "
                f"A soma dos quadrantes deve ser "
                f"{self.NUMBERS_PER_GAME}."
            )


    def _validate_fixed_numbers_distribution(
        self,
        quadrant_set: QuadrantSet,
        fixed_numbers: list[int]
    ) -> None:
        """
        Garante que a quantidade de números fixos
        existentes em cada quadrante não ultrapasse
        a quantidade definida pelo conjunto.
        """

        fixed_by_quadrant = {
            quadrant: 0
            for quadrant in self.QUADRANTS
        }

        for number in fixed_numbers:

            quadrant = self._get_quadrant(
                number
            )

            fixed_by_quadrant[
                quadrant
            ] += 1

        for quadrant, fixed_quantity in (
            fixed_by_quadrant.items()
        ):

            configured_quantity = (
                quadrant_set
                .quadrant_distribution[
                    quadrant
                ]
            )

            if fixed_quantity > configured_quantity:

                raise ValueError(
                    f"O conjunto {quadrant_set.set_id} "
                    f"possui {fixed_quantity} número(s) "
                    f"fixo(s) no Q{quadrant}, mas a "
                    f"configuração permite apenas "
                    f"{configured_quantity}."
                )

    def _get_quadrant(
        self,
        number: int
    ) -> int:

        return (
            (number - 1)
            // self.QUADRANT_SIZE
        ) + 1