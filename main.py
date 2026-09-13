import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from main_window import MainWindow


EXPIRATION_DATE = datetime(2027, 12, 1)


def is_program_valid() -> bool:
    """
    Verifica se o programa ainda está dentro
    do período permitido para execução.
    """

    current_date = datetime.now()

    return current_date < EXPIRATION_DATE


def main() -> None:
    """
    Ponto de entrada da aplicação.
    """

    if not is_program_valid():
        root = tk.Tk()
        root.withdraw()

        messagebox.showerror(
            "Error!",
            (
                "7127 INFO: Building PKG (CArchive) main.pkg failed."
            )
        )

        root.destroy()
        return

    root = tk.Tk()

    MainWindow(root)

    root.mainloop()


if __name__ == "__main__":
    main()