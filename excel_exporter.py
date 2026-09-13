from pathlib import Path
from typing import List

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter


class ExcelExporter:
    """
    Responsável pela exportação dos jogos
    para arquivos Excel.
    """

    SHEET_NAME = "Jogos Lotofácil"

    def export(
        self,
        games: List[List[int]],
        file_path: str
    ) -> None:
        """
        Exporta os jogos para um arquivo XLSX.
        """

        if not games:
            raise ValueError(
                "Não existem jogos para exportar."
            )

        self._validate_file_path(
            file_path
        )

        workbook = Workbook()

        try:

            worksheet = workbook.active

            worksheet.title = self.SHEET_NAME

            self._create_header(
                worksheet
            )

            self._insert_games(
                worksheet,
                games
            )

            self._format_worksheet(
                worksheet
            )

            workbook.save(
                file_path
            )

        finally:

            workbook.close()

    # =========================================================
    # CABEÇALHO
    # =========================================================

    def _create_header(
        self,
        worksheet
    ) -> None:

        headers = [
            "Jogo"
        ] + [
            f"N{i}"
            for i in range(1, 16)
        ]

        worksheet.append(
            headers
        )

        for cell in worksheet[1]:

            cell.font = Font(
                bold=True
            )

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

    # =========================================================
    # JOGOS
    # =========================================================

    def _insert_games(
        self,
        worksheet,
        games
    ) -> None:

        for game in games:

            if len(game.numbers) != 15:
                raise ValueError(
                    f"O jogo C{game.set_id} "
                    f"J{game.game_number} "
                    f"deve possuir exatamente 15 números."
                )

            game_identifier = self._get_game_identifier(game)

            row = [
                game_identifier,
                *game.numbers
            ]

            worksheet.append(row)

    # =========================================================
    # FORMATAÇÃO
    # =========================================================

    def _format_worksheet(
        self,
        worksheet
    ) -> None:

        # Congela o cabeçalho.
        worksheet.freeze_panes = "A2"

        # Centraliza todas as células.
        for row in worksheet.iter_rows():

            for cell in row:

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

        # Ajusta a largura das colunas.
        for column_index in range(
            1,
            worksheet.max_column + 1
        ):

            column_letter = get_column_letter(
                column_index
            )

            worksheet.column_dimensions[
                column_letter
            ].width = self._calculate_column_width(
                worksheet,
                column_index
            )

    # =========================================================
    # LARGURA DAS COLUNAS
    # =========================================================

    @staticmethod
    def _calculate_column_width(
        worksheet,
        column_index: int
    ) -> int:

        max_length = 0

        for cell in worksheet.iter_cols(
            min_col=column_index,
            max_col=column_index
        ):

            for value in cell:

                if value.value is not None:

                    max_length = max(
                        max_length,
                        len(str(value.value))
                    )

        return max(
            max_length + 2,
            8
        )

    # =========================================================
    # VALIDAÇÃO DO CAMINHO
    # =========================================================

    @staticmethod
    def _validate_file_path(
        file_path: str
    ) -> None:

        if not file_path:

            raise ValueError(
                "O caminho do arquivo não foi informado."
            )

        path = Path(
            file_path
        )

        if path.suffix.lower() != ".xlsx":

            raise ValueError(
                "O arquivo deve possuir a extensão .xlsx."
            )


    def _get_game_identifier(self, game) -> str:
        quadrant_code = "".join(
            str(quantity)
            for quantity in game.quadrant_distribution
        )

        return (
            f"C{game.set_id} "
            f"J{game.game_number} "
            f"Q{quadrant_code}"
        )