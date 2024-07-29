from ..main import ttk, Any
from typing import Literal


class HeaderLabel(ttk.Frame):
    """Фрейм - заголовок, с надписью и подчеркиванием."""

    def __init__(
        self, 
        master: Any, 
        text: str = '', 
        anchor: Literal['w', 'n', 'e'] = 'w',
        padx: int = 15
        ):
        super().__init__(master)

        # Разделитель
        ttk.Separator(self, orient='horizontal').place(relwidth=1.0, rely=0.39)

        # Лейбл с текстом
        self.lbl = ttk.Label(self, text=text, padding=(0, -5, 0, -2))
        match anchor:
            case 'n': justify = 0
            case 'e': justify = (0, padx)
            case 'w' | _ : justify = (padx, 0)
        self.lbl.pack(anchor=anchor, padx=justify)
