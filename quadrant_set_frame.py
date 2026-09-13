import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict


class QuadrantSetFrame:
    """
    Componente visual responsável por configurar
    um conjunto de distribuição dos quadrantes.
    """

    def __init__(
        self,
        parent: ttk.Frame,
        set_id: int,
        on_remove: Callable[[int], None]
    ) -> None:

        self.set_id = set_id
        self.on_remove = on_remove

        self.quadrant_vars = {
            quadrant: tk.StringVar()
            for quadrant in range(1, 6)
        }

        self.number_of_games_var = tk.StringVar()

        self.total_var = tk.StringVar(
            value="Total: 0 / 15"
        )

        self.frame = ttk.LabelFrame(
            parent,
            text=f"Conjunto de Quadrantes {set_id}",
            padding=15
        )

        self._create_widgets()

    # =========================================================
    # POSICIONAMENTO
    # =========================================================

    def pack(self, **kwargs) -> None:

        self.frame.pack(
            **kwargs
        )

    # =========================================================
    # WIDGETS
    # =========================================================

    def _create_widgets(self) -> None:

        self._create_quadrants_section()

        self._create_bottom_section()

    # =========================================================
    # QUADRANTES
    # =========================================================

    def _create_quadrants_section(self) -> None:

        quadrants_frame = ttk.Frame(
            self.frame
        )

        quadrants_frame.pack(
            fill=tk.X
        )

        for quadrant in range(1, 6):

            self._create_quadrant_input(
                parent=quadrants_frame,
                quadrant=quadrant
            )

    def _create_quadrant_input(
        self,
        parent: ttk.Frame,
        quadrant: int
    ) -> None:

        container = ttk.Frame(
            parent
        )

        container.pack(
            side=tk.LEFT,
            padx=5,
            expand=True
        )

        label = ttk.Label(
            container,
            text=f"Q{quadrant} do {'1 a 5' if quadrant == 1 else '6 a 10' if quadrant == 2 else '11 a 15' if quadrant == 3 else '16 a 20' if quadrant == 4 else '21 a 25'}"
        )

        label.pack()

        entry = ttk.Entry(
            container,
            textvariable=self.quadrant_vars[
                quadrant
            ],
            width=6,
            justify=tk.CENTER
        )

        entry.pack(
            pady=(5, 0)
        )

        self.quadrant_vars[
            quadrant
        ].trace_add(
            "write",
            self._update_total
        )

    # =========================================================
    # PARTE INFERIOR
    # =========================================================

    def _create_bottom_section(self) -> None:

        bottom_frame = ttk.Frame(
            self.frame
        )

        bottom_frame.pack(
            fill=tk.X,
            pady=(15, 0)
        )

        games_label = ttk.Label(
            bottom_frame,
            text="Quantidade de jogos:"
        )

        games_label.pack(
            side=tk.LEFT
        )

        games_entry = ttk.Entry(
            bottom_frame,
            textvariable=self.number_of_games_var,
            width=8,
            justify=tk.CENTER
        )

        games_entry.pack(
            side=tk.LEFT,
            padx=(8, 20)
        )

        total_label = ttk.Label(
            bottom_frame,
            textvariable=self.total_var,
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        )

        total_label.pack(
            side=tk.LEFT
        )

        remove_button = ttk.Button(
            bottom_frame,
            text="Remover",
            command=self._remove
        )

        remove_button.pack(
            side=tk.RIGHT
        )

    # =========================================================
    # TOTAL
    # =========================================================

    def _update_total(
        self,
        *_args
    ) -> None:

        total = 0

        for variable in self.quadrant_vars.values():

            value = variable.get().strip()

            if value.isdigit():

                total += int(value)

        self.total_var.set(
            f"Total: {total} / 15"
        )

    # =========================================================
    # LEITURA DOS DADOS
    # =========================================================

    def get_quadrant_distribution(
        self
    ) -> Dict[int, int]:

        distribution = {}

        for quadrant, variable in (
            self.quadrant_vars.items()
        ):

            value = variable.get().strip()

            if not value:

                raise ValueError(
                    f"Informe o valor do Q{quadrant} "
                    f"no conjunto {self.set_id}."
                )

            try:

                distribution[quadrant] = int(
                    value
                )

            except ValueError as error:

                raise ValueError(
                    f"Q{quadrant} do conjunto "
                    f"{self.set_id} deve ser um número inteiro."
                ) from error

        return distribution

    def get_number_of_games(self) -> int:

        value = (
            self.number_of_games_var
            .get()
            .strip()
        )

        if not value:

            raise ValueError(
                f"Informe a quantidade de jogos "
                f"do conjunto {self.set_id}."
            )

        try:

            return int(value)

        except ValueError as error:

            raise ValueError(
                f"A quantidade de jogos do conjunto "
                f"{self.set_id} deve ser um número inteiro."
            ) from error

    # =========================================================
    # REMOÇÃO
    # =========================================================

    def _remove(self) -> None:

        self.on_remove(
            self.set_id
        )

        self.frame.destroy()


    def update_set_id(self, new_id: int) -> None:
        self.set_id = new_id

        self.frame.configure(
            text=f"Conjunto de Quadrantes {new_id}"
        )

    def _remove_quadrant_set(self, set_id: int) -> None:
        if set_id not in self.quadrant_set_frames:
            return

        del self.quadrant_set_frames[set_id]

        new_frames = {}

        for new_id, old_id in enumerate(
            sorted(self.quadrant_set_frames.keys()),
            start=1
        ):
            frame = self.quadrant_set_frames[old_id]

            frame.update_set_id(new_id)

            new_frames[new_id] = frame

        self.quadrant_set_frames = new_frames

        self.next_set_id = len(self.quadrant_set_frames) + 1