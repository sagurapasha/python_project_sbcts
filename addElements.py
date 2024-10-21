import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from datetime import datetime
import psycopg2
from dateTimeSelector import DateTimeSelector
from databaseManager import DatabaseManager
from tkcalendar import DateEntry
from toolTip import ToolTip




class AddElements:

    def __init__(self, root):
        self.root = root


# Добавить поле Текст и поле ввода на Вкладку "Информация о ТС (слева)"
    def add_left_entry_info_ts( self, parent, text, value, row, entries_dict, column, key, style):
        # Настройка стиля для неактивного Entry
        style.configure("Disabled.TEntry", fieldbackground="#e0e0e0", font=("Arial", 11))
        tk.Label(parent, text=text, borderwidth=2, relief="groove", height=2).grid(row=row, column=column, padx=(0, 0), sticky="nsew")
        entry = ttk.Entry(parent, width=50,style="Disabled.TEntry")
        entry.grid(row=row, column=column + 1, sticky="nsew", padx=1, pady=1)
        entry.insert(0, str(value) if value else "")
        entries_dict[key] = entry
        entry.config(state="readonly")
        tooltip = ToolTip(entry, entry.get())

    # Добавить поле Текст и поле ввода на Вкладку "Информация о ТС (справа)"
    def add_right_entry_info_ts(self,parent, text, value, row, entries_dict, column, key, style):
        # Настройка стиля для неактивного Entry
        style.configure("Disabled.TEntry", fieldbackground="#e0e0e0", font=("Arial", 11))
        tk.Label(parent, text=text,  borderwidth=2, relief="groove").grid(row=row, column=column,  padx=(0, 0), sticky="nsew")
        entry = ttk.Entry(parent, width=50,style="Disabled.TEntry")
        entry.grid(row=row, column=column + 1, padx=1, pady=1, sticky="nsew")
        entry.insert(0, str(value) if value else "")
        entries_dict[key] = entry
        entry.config(state="readonly")
        tooltip = ToolTip(entry, entry.get())


    # Добавить чекбокс на Вкладку "Информация о ТС (слева)"
    def add_left_checkbox_info_ts(self, parent, text, value, row, checkbox_dict, column, key, checkbox_document):

        # Создаем фрейм с границами, чтобы чекбокс выглядел как внутри рамки
        container = tk.Frame(parent, borderwidth=2, relief="groove")
        container.grid(row=row, column=column, columnspan=2, padx=0, pady=0, sticky="nswe")

        # Создаем переменную для состояния чекбокса
        checkbox_var = tk.BooleanVar(value=value)
        checkbox = ttk.Checkbutton(container, text=text, variable=checkbox_var)
        checkbox.pack(expand=True, fill="both")  # Размещаем чекбокс внутри контейнера

        # Устанавливаем начальное значение и сохраняем переменную в словарь
        checkbox_var.set(value)
        checkbox_dict[key] = checkbox_var
        checkbox_document[key] = checkbox

        # Отключаем чекбокс, если нужно
        checkbox.config(state="disabled")

    # Добавить чекбокс на Вкладку "Информация о ТС (справа)"
    def add_right_checkbox_info_ts(self, parent, text, value, row, checkbox_dict, column, key, checkbox_document):
        """Добавляет чекбокс в правый столбец с начальным значением False и границей."""

        # Создаем фрейм-контейнер с границей, чтобы чекбокс выглядел как внутри рамки
        container = tk.Frame(parent, borderwidth=2, relief="groove")
        container.grid(row=row, column=column, columnspan=2, pady=0, sticky="nswe")

        # Создаем переменную для состояния чекбокса
        checkbox_var = tk.BooleanVar(value=value)

        # Создаем чекбокс внутри контейнера
        checkbox = ttk.Checkbutton(container, text=text, variable=checkbox_var, style="TCheckbutton")
        checkbox.pack(expand=True, fill="both")  # Размещаем чекбокс внутри контейнера

        # Устанавливаем начальное значение и сохраняем переменную в словарь
        checkbox_var.set(value)
        checkbox_dict[key] = checkbox_var
        checkbox_document[key] = checkbox

        # Отключаем чекбокс, если нужно
        checkbox.config(state="disabled")

    # Добавить сколбак
    def create_scrollable_frame(self,parent):
        # Создаем Canvas и Scrollbar для прокрутки
        canvas = tk.Canvas(parent, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Настраиваем прокрутку
        canvas.configure(yscrollcommand=scrollbar.set)

        # Размещаем Frame внутри Canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Связываем событие изменения размера фрейма с прокруткой
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Устанавливаем размеры Canvas в соответствии с размерами родительского контейнера
        parent.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw",
                                     width=parent.winfo_width())
            )
        )

        # Привязываем прокрутку колесиком мыши
        def _on_mouse_wheel(event):
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        # Привязываем прокрутку колесиком к canvas и родительскому фрейму
        scrollable_frame.bind_all("<MouseWheel>", _on_mouse_wheel)

        # Размещаем Canvas и Scrollbar в родительском фрейме
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame