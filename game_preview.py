import tkinter as tk
from tkinter import ttk
from typing import Callable, List


class GamePreview:
    """
    Janela responsável por apresentar os jogos
    gerados antes da exportação.
    """

    WINDOW_TITLE = "Preview dos Jogos"
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 600

    def __init__(
        self,
        parent: tk.Tk,
        games: List[List[int]],
        on_confirm: Callable[[List[List[int]]], bool]
    ) -> None:

        self.parent = parent
        self.games = games
        self.on_confirm = on_confirm

        self.window = tk.Toplevel(
            parent
        )

        self._configure_window()
        self._create_widgets()

    # =========================================================
    # CONFIGURAÇÃO
    # =========================================================

    def _configure_window(self) -> None:

        self.window.title(
            self.WINDOW_TITLE
        )

        self.window.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        )

        self.window.minsize(
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT
        )

        self.window.transient(
            self.parent
        )

        self.window.grab_set()

    # =========================================================
    # WIDGETS
    # =========================================================

    def _create_widgets(self) -> None:

        main_frame = ttk.Frame(
            self.window,
            padding=20
        )

        main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        self._create_header(
            main_frame
        )

        self._create_table(
            main_frame
        )

        self._create_actions(
            main_frame
        )

    # =========================================================
    # CABEÇALHO
    # =========================================================

    def _create_header(
        self,
        parent: ttk.Frame
    ) -> None:

        title = ttk.Label(
            parent,
            text="Preview dos Jogos Gerados",
            font=(
                "Segoe UI",
                16,
                "bold"
            )
        )

        title.pack(
            anchor=tk.W
        )

        description = ttk.Label(
            parent,
            text=(
                f"{len(self.games)} jogo(s) foram gerados. "
                "Confira os resultados antes de continuar."
            )
        )

        description.pack(
            anchor=tk.W,
            pady=(5, 15)
        )

    # =========================================================
    # TABELA
    # =========================================================

    def _create_table(
        self,
        parent: ttk.Frame
    ) -> None:

        table_frame = ttk.Frame(
            parent
        )

        table_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        columns = [
            "game"
        ] + [
            f"n{i}"
            for i in range(1, 16)
        ]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "game",
            text="Jogo"
        )

        self.tree.column(
            "game",
            width=60,
            anchor=tk.CENTER
        )

        for index in range(1, 16):

            column = f"n{index}"

            self.tree.heading(
                column,
                text=f"N{index}"
            )

            self.tree.column(
                column,
                width=45,
                anchor=tk.CENTER
            )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.HORIZONTAL,
            command=self.tree.xview
        )

        self.tree.configure(
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        self._populate_table()

    # =========================================================
    # PREENCHER TABELA
    # =========================================================

    def _populate_table(self) -> None:

        for game in self.games:
            game_identifier = self._get_game_identifier(game)

            values = [
                game_identifier,
                *game.numbers
            ]

            self.tree.insert(
                "",
                tk.END,
                values=values
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

    # =========================================================
    # AÇÕES
    # =========================================================

    def _create_actions(
        self,
        parent: ttk.Frame
    ) -> None:

        frame = ttk.Frame(
            parent
        )

        frame.pack(
            fill=tk.X,
            pady=(15, 0)
        )

        cancel_button = ttk.Button(
            frame,
            text="Cancelar",
            command=self._on_cancel
        )

        cancel_button.pack(
            side=tk.LEFT
        )

        export_button = ttk.Button(
            frame,
            text="Confirmar e Gerar Planilha",
            command=self._on_confirm
        )

        export_button.pack(
            side=tk.RIGHT
        )

    # =========================================================
    # EVENTOS
    # =========================================================

    def _on_cancel(self) -> None:

        self.window.destroy()

    def _on_confirm(self) -> None:

        exported = self.on_confirm(
            self.games
        )

        if exported:
            self.window.destroy()