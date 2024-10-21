import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from datetime import datetime

class DateTimeSelector:
    def __init__(self, root):
        self.root = root

    def open_calendar(self, entry, button):
        def select_date():
            selected_date = cal.get_date()
            entry.delete(0, tk.END)
            entry.insert(0, selected_date)
            calendar_window.destroy()

        # Создаем всплывающее окно для календаря
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Выбор даты")
        calendar_window.grab_set()

        # Получение координат кнопки для позиционирования окна календаря над кнопкой
        x = button.winfo_rootx()
        y = button.winfo_rooty()

        calendar_window.geometry(f"+{x}+{y}")  # Позиционирование окна календаря над кнопкой
        cal = Calendar(calendar_window, selectmode="day", year=datetime.now().year, month=datetime.now().month,
                       day=datetime.now().day, date_pattern="yyyy-mm-dd")
        cal.pack(pady=20)

        select_button = tk.Button(calendar_window, text="Выбрать", command=select_date)
        select_button.pack(pady=10)


    def open_time_selector(self, entry, button):
        def select_time():
            selected_time = f"{hour_combobox.get()}:{minute_combobox.get()}"
            entry.delete(0, tk.END)
            entry.insert(0, selected_time)
            time_window.destroy()

        # Создаем всплывающее окно для выбора времени
        time_window = tk.Toplevel(self.root)
        time_window.title("Выбор времени")
        time_window.grab_set()

        # Получение координат кнопки для позиционирования окна времени над кнопкой
        x = button.winfo_rootx()
        y = button.winfo_rooty()

        time_window.geometry(f"+{x}+{y-100}")  # Позиционирование окна времени над кнопкой

        # Выпадающие списки для выбора часов и минут
        hours = [f"{i:02}" for i in range(24)]  # часы от 00 до 23
        minutes = [f"{i:02}" for i in range(60)]  # минуты от 00 до 59

        hour_combobox = ttk.Combobox(time_window, values=hours, width=5, font=("Arial", 16))
        hour_combobox.set("00")  # Установка текущего времени по умолчанию
        hour_combobox.grid(row=0, column=0, padx=5, pady=10)

        minute_combobox = ttk.Combobox(time_window, values=minutes, width=5, font=("Arial", 16))
        minute_combobox.set("00")
        minute_combobox.grid(row=0, column=1, padx=5, pady=10)

        select_button = tk.Button(time_window, text="Выбрать время", command=select_time)
        select_button.grid(row=1, column=0, columnspan=2, pady=10)


