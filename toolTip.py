import tkinter as tk
from tkinter import ttk

class ToolTip:
    """Класс для создания всплывающей подсказки."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Создает окно всплывающей подсказки под курсором."""
        if self.tooltip_window or not self.text:
            return
        x = event.x_root + 10  # Позиция всплывающей подсказки по оси X
        y = event.y_root + 10  # Позиция всплывающей подсказки по оси Y
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Убирает рамки окна
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="white", relief="solid", borderwidth=1)
        label.pack(ipadx=5, ipady=2)

    def hide_tooltip(self, event=None):
        """Закрывает окно всплывающей подсказки."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
