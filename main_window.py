import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List

from game_config import GameConfig
from generated_game import GeneratedGame
from quadrant_set import QuadrantSet
from quadrant_set_frame import QuadrantSetFrame
from validator import GameValidator

from game_generator import GameGenerator
from game_preview import GamePreview

from tkinter import filedialog
from excel_exporter import ExcelExporter
from typing import List


class MainWindow:

    WINDOW_TITLE = "Gerador de Jogos - Lotofácil"
    WINDOW_WIDTH = 850
    WINDOW_HEIGHT = 750

    def __init__(self, root: tk.Tk) -> None:

        self.root = root

        self.validator = GameValidator()
        self.generator = GameGenerator()
        self.exporter = ExcelExporter()


        self._create_variables()
        self._configure_window()
        self._create_widgets()
        self.quadrant_set_frames = {}


    # =========================================================
    # CONFIGURAÇÃO DA JANELA
    # =========================================================

    def _configure_window(self) -> None:

        self.root.title(
            self.WINDOW_TITLE
        )

        self.root.geometry(
            f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}"
        )

        self.root.minsize(
            self.WINDOW_WIDTH,
            self.WINDOW_HEIGHT
        )

        self.root.resizable(
            True,
            True
        )

    # =========================================================
    # VARIÁVEIS
    # =========================================================

    def _create_variables(self) -> None:
        self.fixed_numbers_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Aguardando configuração..."
        )

        self.quadrant_set_frames = {}

        self.next_set_id = 1

    # =========================================================
    # WIDGETS
    # =========================================================

    def _create_widgets(self) -> None:

        self._create_main_frame()

        self._create_header()

        self._create_fixed_numbers_section()

        self._create_quadrant_sets_section()

        self._create_actions_section()

    # =========================================================
    # FRAME PRINCIPAL
    # =========================================================

    def _create_main_frame(self) -> None:

        self.main_frame = ttk.Frame(
            self.root,
            padding=25
        )

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

    # =========================================================
    # CABEÇALHO
    # =========================================================

    def _create_header(self) -> None:

        title = ttk.Label(
            self.main_frame,
            text="Gerador de Jogos da Lotofácil",
            font=(
                "Segoe UI",
                20,
                "bold"
            )
        )

        title.pack(
            pady=(0, 5)
        )

        subtitle = ttk.Label(
            self.main_frame,
            text=(
                "Configure os números fixos e a distribuição "
                "dos números por quadrante."
            ),
            font=(
                "Segoe UI",
                10
            )
        )

        subtitle.pack(
            pady=(0, 20)
        )

    # =========================================================
    # NÚMEROS FIXOS
    # =========================================================

    def _create_fixed_numbers_section(self) -> None:

        frame = ttk.LabelFrame(
            self.main_frame,
            text="Números Fixos",
            padding=15
        )

        frame.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        description = ttk.Label(
            frame,
            text=(
                "Informe os números que devem aparecer "
                "em todos os jogos."
            )
        )

        description.pack(
            anchor=tk.W,
            pady=(0, 8)
        )

        self.fixed_numbers_entry = ttk.Entry(
            frame,
            textvariable=self.fixed_numbers_var,
            font=("Segoe UI", 11)
        )

        self.fixed_numbers_entry.pack(
            fill=tk.X
        )

        hint = ttk.Label(
            frame,
            text="Exemplo: 1, 5, 8, 12, 20",
            font=(
                "Segoe UI",
                9
            )
        )

        hint.pack(
            anchor=tk.W,
            pady=(5, 0)
        )


    def _create_quadrant_sets_section(self) -> None:

        section_frame = ttk.LabelFrame(
            self.main_frame,
            text="Conjuntos de Quadrantes",
            padding=10
        )

        section_frame.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(0, 10)
        )

        # =====================================================
        # CANVAS
        # =====================================================

        self.sets_canvas = tk.Canvas(
            section_frame,
            highlightthickness=0
        )

        vertical_scrollbar = ttk.Scrollbar(
            section_frame,
            orient=tk.VERTICAL,
            command=self.sets_canvas.yview
        )

        self.quadrant_sets_container = ttk.Frame(
            self.sets_canvas
        )

        self.quadrant_sets_container.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.canvas_window = self.sets_canvas.create_window(
            (0, 0),
            window=self.quadrant_sets_container,
            anchor="nw"
        )

        self.sets_canvas.configure(
            yscrollcommand=vertical_scrollbar.set
        )

        self.sets_canvas.bind(
            "<Configure>",
            self._resize_canvas_content
        )

        self.sets_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.sets_canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        vertical_scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )



        # =====================================================
        # BOTÃO ADICIONAR
        # =====================================================

        add_button = ttk.Button(
            self.main_frame,
            text="+ Adicionar Conjunto",
            command=self._add_quadrant_set
        )

        add_button.pack(
            anchor=tk.W,
            pady=(0, 15)
        )

    def _on_mousewheel(self, event) -> None:
            """Rola a tela verticalmente ao usar a roda do mouse."""
            # No Windows/macOS, event.delta é usado para identificar a direção do scroll
            self.sets_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_scroll_region(
        self,
        _event=None
    ) -> None:

        self.sets_canvas.configure(
            scrollregion=self.sets_canvas.bbox(
                "all"
            )
        )

    def _resize_canvas_content(
        self,
        event
    ) -> None:

        self.sets_canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )


    # =========================================================
    # BOTÕES
    # =========================================================
    def _create_actions_section(self) -> None:

        frame = ttk.Frame(
            self.main_frame
        )

        frame.pack(
            fill=tk.X,
            pady=(15, 0)
        )

        buttons_frame = ttk.Frame(
            frame
        )

        buttons_frame.pack(
            fill=tk.X
        )

        self.validate_button = ttk.Button(
            buttons_frame,
            text="Validar Configuração",
            command=self._on_validate
        )

        self.validate_button.pack(
            side=tk.LEFT,
            padx=(0, 10)
        )

        self.generate_button = ttk.Button(
            buttons_frame,
            text="Gerar Planilha",
            command=self._on_generate
        )

        self.generate_button.pack(
            side=tk.LEFT
        )

        self.status_var = tk.StringVar(
            value="Aguardando configuração..."
        )

        status_label = ttk.Label(
            frame,
            textvariable=self.status_var,
            font=(
                "Segoe UI",
                9
            )
        )

        status_label.pack(
            anchor=tk.W,
            pady=(10, 0)
        )

    # =========================================================
    # LEITURA DA CONFIGURAÇÃO
    # =========================================================

    def _build_config(self) -> GameConfig:
        """
        Converte os valores da interface para um GameConfig.
        """

        fixed_numbers = (
            self._parse_fixed_numbers()
        )

        number_of_games = (
            self._parse_number_of_games()
        )

        quadrant_distribution = (
            self._parse_quadrant_distribution()
        )

        return GameConfig(
            fixed_numbers=fixed_numbers,
            number_of_games=number_of_games,
            quadrant_distribution=quadrant_distribution
        )

    # =========================================================
    # NÚMEROS FIXOS
    # =========================================================

    def _parse_fixed_numbers(self) -> list[int]:
        """
        Converte o campo de números fixos
        em uma lista de números inteiros.
        """

        value = (
            self.fixed_numbers_var
            .get()
            .strip()
        )

        if not value:

            return []

        normalized_value = value.replace(
            ";",
            ","
        )

        numbers = []

        for item in normalized_value.split(","):

            item = item.strip()

            if not item:

                continue

            try:

                numbers.append(
                    int(item)
                )

            except ValueError as error:

                raise ValueError(
                    f"'{item}' não é um número válido."
                ) from error

        return numbers

    # =========================================================
    # BOTÃO VALIDAR
    # =========================================================

    def _on_validate(self) -> None:

        try:

            config = self._build_config()

            self.validator.validate(
                config
            )

            self.status_var.set(
                "Configuração válida."
            )

            messagebox.showinfo(
                "Configuração válida",
                "A configuração foi validada com sucesso."
            )

        except ValueError as error:

            self.status_var.set(
                "Configuração inválida."
            )

            messagebox.showerror(
                "Erro de validação",
                str(error)
            )

    # =========================================================
    # BOTÃO GERAR
    # =========================================================

    def _on_generate(self) -> None:

        try:

            config = self._build_config()

            self.validator.validate(
                config
            )

            games = self.generator.generate(
                config
            )

            self.status_var.set(
                f"{len(games)} jogos gerados."
            )

            GamePreview(
                parent=self.root,
                games=games,
                on_confirm=self._export_games
            )

        except ValueError as error:

            self.status_var.set(
                "Configuração inválida."
            )

            messagebox.showerror(
                "Configuração inválida",
                str(error)
            )

        except Exception as error:

            self.status_var.set(
                "Erro ao gerar os jogos."
            )

            messagebox.showerror(
                "Erro",
                f"Não foi possível gerar os jogos.\n\n{error}"
            )


    def _export_games(
        self,
        games: List[GeneratedGame]
    ) -> bool:
        """
        Abre o diálogo para escolha do arquivo
        e exporta os jogos para Excel.
        """

        file_path = filedialog.asksaveasfilename(
            parent=self.root,
            title="Salvar jogos da Lotofácil",
            defaultextension=".xlsx",
            filetypes=[
                (
                    "Arquivo Excel",
                    "*.xlsx"
                ),
                (
                    "Todos os arquivos",
                    "*.*"
                )
            ],
            initialfile="jogos_lotofacil.xlsx"
        )

        if not file_path:
            return False

        try:
            self.exporter.export(
                games,
                file_path
            )

        except (ValueError, OSError) as error:
            messagebox.showerror(
                "Erro ao exportar",
                (
                    "Não foi possível gerar a planilha.\n\n"
                    f"{error}"
                ),
                parent=self.root
            )

            return False

        except Exception as error:
            messagebox.showerror(
                "Erro inesperado",
                (
                    "Ocorreu um erro inesperado ao gerar "
                    "a planilha.\n\n"
                    f"{type(error).__name__}: {error}"
                ),
                parent=self.root
            )

            return False

        messagebox.showinfo(
            "Exportação concluída",
            (
                "A planilha foi gerada com sucesso!\n\n"
                f"Arquivo:\n{file_path}"
            ),
            parent=self.root
        )

        self.status_var.set(
            "Planilha gerada com sucesso."
        )

        return True



    def _add_quadrant_set(self) -> None:

        set_id = self.next_set_id

        quadrant_set_frame = QuadrantSetFrame(
            parent=self.quadrant_sets_container,
            set_id=set_id,
            on_remove=self._remove_quadrant_set
        )

        quadrant_set_frame.pack(
            fill=tk.X,
            pady=(0, 10)
        )

        self.quadrant_set_frames[
            set_id
        ] = quadrant_set_frame

        self.next_set_id += 1

    def _remove_quadrant_set(self, set_id: int) -> None:
        if set_id not in self.quadrant_set_frames:
            return

        # Remove o conjunto
        del self.quadrant_set_frames[set_id]

        # Renumera os conjuntos restantes
        new_frames = {}

        for new_id, old_id in enumerate(
            sorted(self.quadrant_set_frames.keys()),
            start=1
        ):
            frame = self.quadrant_set_frames[old_id]

            frame.set_id = new_id
            frame.frame.configure(
                text=f"Conjunto de Quadrantes {new_id}"
            )

            new_frames[new_id] = frame

        self.quadrant_set_frames = new_frames

        # Atualiza o próximo ID
        self.next_set_id = len(self.quadrant_set_frames) + 1

    def _build_config(self) -> GameConfig:
        """
        Lê os dados da interface e cria a configuração
        completa dos jogos.
        """

        fixed_numbers = self._parse_fixed_numbers()

        quadrant_sets = []

        for set_id in sorted(
            self.quadrant_set_frames
        ):

            set_frame = (
                self.quadrant_set_frames[set_id]
            )

            quadrant_set = QuadrantSet(
                set_id=set_id,

                number_of_games=(
                    set_frame.get_number_of_games()
                ),

                quadrant_distribution=(
                    set_frame
                    .get_quadrant_distribution()
                )
            )

            quadrant_sets.append(
                quadrant_set
            )

        return GameConfig(
            fixed_numbers=fixed_numbers,
            quadrant_sets=quadrant_sets
        )