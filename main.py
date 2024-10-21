import tkinter as tk
from tkinter import messagebox, ttk

from pip._vendor.rich import padding
from tkcalendar import Calendar
import psycopg2
from dateTimeSelector import DateTimeSelector
from databaseManager import DatabaseManager
from addElements import AddElements
from tkcalendar import DateEntry
from toolTip import ToolTip
from tkinter.ttk import Style
import datetime


# Создаем экземпляр класса DatabaseManager
db_manager = DatabaseManager("192.168.2.111", "expert_sbcts", "registry","admin", "Eon7a27i1ZczZ59onvFQ")


# Основное окно
root = tk.Tk()
root.title("Программа управления заявками")
root.geometry("1440x900")  # Размер окна

# Задаем стиль для ttk элементов
style = ttk.Style()
style.theme_use("clam")  # Используем тему 'clam' для современного вида

# Основная рамка для всего интерфейса
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

print ("sd")

# Левая панель
left_panel = tk.Frame(main_frame, width=205, bg="lightgrey", bd=2, relief="groove")  # Добавляем рамку и стиль
left_panel.pack(side="left", fill="y", padx=1, pady=1)  # Добавляем отступы (10 пикселей с каждой стороны)
left_panel.pack_propagate(False)  # Отключаем автоизменение размера

# Правая рабочая область
right_panel = tk.Frame(main_frame)
right_panel.pack(side="right", fill="both", expand=True)

# Создаем несколько фреймов для разных вкладок
application_frame = tk.Frame(right_panel)
sbcts_archive_frame = tk.Frame(right_panel)
settings_frame = tk.Frame(right_panel)

asdasdas

asddasdas

dasdasdas
dasdas

# Переменные стиля

label_style = {"font": ("Arial", 16), "bg": "white"}
entry_style = {"width": 40, "font": ("Arial", 12), "relief": "sunken", "bd": 2, "highlightthickness": 2}
button_style = {"font": ("Arial", 16),  "activebackground": "blue"}

label_style_archive = {"font": ("Arial", 12)}
entry_style_archive = { "font": ("Arial", 12), "relief": "sunken", "bd": 2, "highlightthickness": 2}

# Добавление вкладок и привязка к изменению контента
buttons = ["Список заявок",  "Поиск СБКТС", "Настройки"]
for btn in buttons:
    button = ttk.Button(left_panel, text=btn, command=lambda b=btn: change_content(b))
    button.pack(pady=2, padx=(5, 5), fill="both")




def create_tab3(notebook, result, id, date_time_selector, addElements):

    # Создаем вкладку
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Информация о ТС")

    container_frame_tab1 = ttk.Frame(tab1)
    container_frame_tab1.pack(expand=True, fill="both", anchor="center", padx=0, pady=0)




    # Используем функцию для создания прокручиваемого фрейма
    form_frame_tab1 = addElements.create_scrollable_frame(container_frame_tab1)

    form_frame_tab1.columnconfigure(0, weight=1)  # Левая колонка
    form_frame_tab1.columnconfigure(1, weight=1)  # Колонка между метками, занимает все доступное пространство
    form_frame_tab1.columnconfigure(2, weight=1)  # Правая колонка
    form_frame_tab1.columnconfigure(3, weight=1)  # Правая колонка

    # Словарь общие данные
    main_data = {
        "vin": ["Идентификационный номер (VIN)", result.get('vin'), "left"],
        "customer": ["Заказчик", result.get('customer'), "left"],
        "owner": ["Собственник", result.get('owner'), "left"],
        "customer_address": ["Адрес заказчика", result.get('customer_address'), "left"],
        "actual_address": ["Фактический адрес (для юр. лиц)", result.get('actual_address'), "left"],
        "contact_phone": ["Контактный телефон", result.get('contact_phone'), "left"],
        "inn": ["ИНН", result.get('inn'), "left"],
        "kpp": ["КПП", result.get('kpp'), "left"],
        "ogrn": ["ОГРН/ОГРНИП", result.get('ogrn'), "left"],
        "email": ["ОГРН/ОГРНИП", result.get('email'), "left"],
        "delegate": ["Представитель заявителя (доверенное лицо)", result.get('delegate'), "left"],
        "identity_document": ["Документ, удостоверяющий личность представителя", result.get('identity_document'),
                              "left"],
        "power_of_attorney": ["Доверенность", result.get('power_of_attorney'), "left"],
        "dogovor": ["Договор (при наличии)", result.get('dogovor'), "right"],
        "date_registration": ["Дата оформления заявки", result.get('date_registration'), "right"],
        "date_submission": ["Дата предоставления ТС", result.get('date_submission'), "right"],
        "time_submission": ["Время предоставления ТС", result.get('time_submission'), "right"],
        "sbcts_num": ["Номер СБКТС", result.get('sbcts_num'), "right"],
        "date_sbcts": ["Дата СБКТС", result.get('date_sbcts'), "right"],
        "epts_num": ["Номер электронного ПТС", result.get('epts_num'), "right"],
        "epts_date": ["Дата электронного ПТС", result.get('epts_date'), "right"],
        "ets_num": ["Номер ETC", result.get('ets_num'), "right"],
        "status": ["Статус", result.get('status'), "right"]
    }

    # Предоставленные документы
    document_data = {
        "applicant_doc_1": ["Документ, удостоверяющий заявителя", result.get('applicant_doc_1'), "left"],
        "applicant_doc_2": ["Документ, подтверждающий право владения, или пользования и (или) распоряжения транспортным средством", result.get('applicant_doc_2'), "left"],
        "technical_description": ["Общее техническое описание транспортного средства", result.get('technical_description'), "left"],
        "doc_vin": ["Документ о присвоениии идентификационного номера транспортного средства (при наличии)", result.get('doc_vin'), "left"],
        "copies_of_certificates": ["Копии сертификатов на компоненты (при наличии)", result.get('copies_of_certificates'), "right"],
        "technical_documentation": ["Конструкторская, либо иная тех. документация по которой изготавливается продукция (при наличии)", result.get('technical_documentation'), "right"],
        "drawings": ["Чертежи оригинальных деталей и тех. карты их производства, либо соответ. эскизная док. (при наличии)", result.get('drawings'), "right"],
        "other_documents": ["Иная документация (при наличии)", result.get('other_documents'), "right"]
     }

    # Словарь параметры ОС улица
    environmental_data_outside = {
        "temperature": ["– температура окружающего воздуха t, ºС", result.get('temperature'), "right"],
        "pressure_kpa": ["– атмосферное давление  кПа (мм.рт.ст.)", result.get('pressure_kpa'), "right"],
        "pressure_mm": ["– атмосферное давление мм.рт.ст.", result.get('pressure_mm'), "right"],
        "humidity": ["– относительная влажность воздуха φ, %", result.get('humidity'), "right"]
    }

    # Словарь параметры ОС бокс
    environmental_data_box = {
        "temperature": ["– температура окружающего воздуха t, ºС", result.get('temperature'), "left"],
        "pressure_kpa": ["– атмосферное давление  кПа", result.get('pressure_kpa'), "left"],
        "pressure_mm": ["– атмосферное давление мм.рт.ст.", result.get('pressure_mm'), "left"],
        "humidity": ["– относительная влажность воздуха φ, %", result.get('humidity'), "left"],
        "voltage_380_min": ["- напряжение, В", result.get('voltage_380_min'), "left"],
        "frequency_380_min": ["- частота электрического тока, Гц", result.get('frequency_380_min'), "left"],
        "voltage_1f_380v": ["- 1ф 380В Напряжение ч/л", result.get('voltage_1f_380v'), "left"],
        "voltage_2f_380v": ["- 2ф 380В Напряжение ч/л", result.get('voltage_2f_380v'), "left"],
        "voltage_3f_380v": ["- 3ф 380В Напряжение ч/л", result.get('voltage_3f_380v'), "left"],
        "voltage_220v": ["- 220В Напряжение ч/л", result.get('voltage_220v'), "left"],
        "frequency_1f_380v": ["- 1ф 380В Частота ч/л", result.get('frequency_1f_380v'), "left"],
        "frequency_2f_380v": ["- 2ф 380В Частота ч/л", result.get('frequency_2f_380v'), "left"],
        "frequency_3f_380v": ["- 3ф 380В Частота ч/л", result.get('frequency_3f_380v'), "left"],
        "frequency_220v": ["- 220В Напряжение ч/л", result.get('frequency_220v'), "left"]
    }

        # Словарь информация о ТС
    vehicle_data = {
        "brand": ["Марка транспортного средства", result.get('brand'), "left"],
        "model": ["Коммерческое наименование", result.get('model'), "left"],
        "type": ["Тип", result.get('type'), "left"],
        "chassis": ["Шасси транспортного средства", result.get('chassis'), "left"],
        "color": ["Цвет", result.get('color'), "left"],
        "year": ["Год выпуска", result.get('year'), "left"],
        "category": ["Категория транспортного средства", result.get('category'), "left"],
        "eco_class": ["Экологический класс", result.get('eco_class'), "left"],
        "manufacturer_address": ["Изготовитель транспортного средства", result.get('manufacturer_address'), "left"],
        "assembly_plant_address": ["Сборочный завод и его адрес", result.get('assembly_plant_address'), "left"],
        "wheel_formula": ["Колесная формула / ведущие колеса", result.get('wheel_formula'), "left"],
        "layout_scheme": ["Схема компоновки транспортного средства", result.get('layout_scheme'), "left"],
        "body_type": ["Тип кузова / количество дверей (для категории М1)", result.get('body_type'), "left"],
        "seating_capacity": ["Количество мест спереди / сзади (для категории М1)", result.get('seating_capacity'),
                             "left"],
        "izp": ["Исполнение загрузочного пространства (для категории N)", result.get('izp'), "left"],
        "cabin": ["Кабина (для категории N)", result.get('cabin'), "left"],
        "passenger_capacity": ["Пассажировместимость (для категорий М2, М3)", result.get('passenger_capacity'), "left"],
        "luggage_volume": ["Общий объем багажных отделений (для категории М3 класса III)", result.get('luggage_volume'), "left"],
        "seating_capacity": ["Количество мест для сидения (для категорий М2, М3, L)", result.get('seating_capacity'), "left"],
        "frame": ["Рама (для категории L)", result.get('frame'), "left"],
        "axes_count": ["Количество осей / колес (для категории О)", result.get('axes_count'), "left"],
        "vehicle_weight": ["Масса ТС в снаряженном состоянии, кг", result.get('vehicle_weight'),
                           "left"],
        "max_weight": ["Технически допустимая максимальная масса ТС, кг",
                       result.get('max_weight'), "left"],
        "length": ["- длина", result.get('length'), "left"],
        "width": ["- ширина", result.get('width'), "left"],
        "height": ["- высота", result.get('height'), "left"],
        "wheelbase": ["База, мм", result.get('wheelbase'), "left"],
        "track": ["Колея передних / задних колес, мм", result.get('track'), "left"],
        "hybrid": ["Описание гибридного транспортного средства", result.get('hybrid'), "left"],
        "front_suspension": ["- передняя", result.get('front_suspension'), "left"],
        "rear_suspension": ["- задняя", result.get('rear_suspension'), "left"],
        "engine": ["Двигатель внутреннего сгорания (марка, тип)", result.get('engine'), "right"],
        "cylinders": ["- количество и расположение цилиндров", result.get('cylinders'), "right"],
        "displacement": ["- рабочий объем цилиндров, см3", result.get('displacement'), "right"],
        "compression_ratio": ["- степень сжатия", result.get('compression_ratio'), "right"],
        "power": ["- максимальная мощность, кВт (мин – 1)", result.get('power'), "right"],
        "fuel": ["Топливо", result.get('fuel'), "right"],
        "fuel_system": ["Система питания (тип)", result.get('fuel_system'), "right"],
        "ignition_system": ["Система зажигания (тип)", result.get('power'), "right"],
        "exhaust_system": ["Система выпуска и нейтрализации отработавших газов", result.get('exhaust_system'), "right"],
        "e_engine_1": ["Электродвигатель электромобиля (марка, тип) 1", result.get('e_engine_1'), "right"],
        "voltage_1": ["Рабочее напряжение, В", result.get('voltage_1'), "right"],
        "max_30_power_1": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_1'), "right"],
        "e_engine_2": ["Электродвигатель электромобиля (марка, тип) 2", result.get('e_engine_2'), "right"],
        "voltage_2": ["Рабочее напряжение, В", result.get('voltage_2'), "right"],
        "max_30_power_2": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_2'), "right"],
        "energy_battery": ["Устройство накопления энергии (только для электромобилей)", result.get('energy_battery'), "right"],
        "e_car": ["Электромашина: (марка, тип)", result.get('e_car'), "right"],
        "voltage": ["Рабочее напряжение, В", result.get('voltage'), "right"],
        "max_30_power": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power'), "right"],
        "clutch": ["Сцепление (марка, тип)", result.get('clutch'), "right"],
        "transmission": ["Трансмиссия", result.get('transmission'), "right"],
        "gearbox": ["Коробка передач (марка, тип)", result.get('gearbox'), "right"],
        "steering": ["Рулевое управление (марка, тип)", result.get('steering'), "right"],
        "working_brake": ["- рабочая", result.get('working_brake'), "right"],
        "spare_brake": ["-запасная", result.get('spare_brake'), "right"],
        "parking_brake": ["- стояночная", result.get('parking_brake'), "right"],
        "tires": ["Шины (обозначение размера)", result.get('tires'), "right"],
        "equipment": ["Дополнительное оборудование", result.get('equipment'), "right"]
    }

    save_button = tk.Button(form_frame_tab1, text="Сформировать АКТ", font=("Arial", 16))
    save_button.grid(row=0, column=0,  pady=(10, 10),  padx=(50, 0), sticky="nsew")

    save_button = tk.Button(form_frame_tab1, text="Сформировать АКТ", font=("Arial", 16))
    save_button.grid(row=0, column=1, pady=(10, 10),  sticky="nsew")

    save_button = tk.Button(form_frame_tab1, text="Сформировать АКТ", font=("Arial", 16))
    save_button.grid(row=0, column=2, pady=(10, 10), sticky="nsew")

    save_button = tk.Button(form_frame_tab1, text="Сформировать АКТ", font=("Arial", 16))
    save_button.grid(row=0, column=3, pady=(10, 10),  padx=(0, 50), sticky="nsew")




    # Заголовок формы Общие данные
    header_label_tab1 = ttk.Label(form_frame_tab1, text="Общие данные", font=("Arial", 16, "bold"))
    header_label_tab1.grid(row=1, column=0, columnspan=4, pady=(15, 10), sticky="")

    # Индексы строк
    i = 2
    k = 2

    # Создание элементов Общие данные
    for key, values in main_data.items():

        if values[0] == "Дата оформления заявки":
            ttk.Label(form_frame_tab1,text=  "Дата оформления заявки", style="Custom.TLabel").grid(row=k, column=2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame_tab1, style="Custom.TEntry", width=34)
            entry.grid(row=k, column=3, padx=0, pady=5, sticky="w")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_registration"] = entry
            date_registration_button = ttk.Button(form_frame_tab1, width=14,  text="Выбрать дату",
                                                 command=lambda: date_time_selector.open_calendar(
                                                     entries_main["date_registration"], date_registration_button))
            date_registration_button.grid(row=k, column=3, padx=(216, 0), pady=5, sticky="w")
            k += 1

        elif values[0] == "Дата предоставления ТС":
            ttk.Label(form_frame_tab1,text=  "Дата предоставления ТС", style="Custom.TLabel").grid(row=k, column=2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame_tab1, style="Custom.TEntry", width=34)
            entry.grid(row=k, column=3, padx=0, pady=5, sticky="w")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_submission"] = entry
            date_registration_button = ttk.Button(form_frame_tab1, width=14,  text="Выбрать дату",
                                                 command=lambda: date_time_selector.open_calendar(
                                                     entries_main["date_submission"], date_registration_button))
            date_registration_button.grid(row=k, column=3, padx=(216, 0), pady=5, sticky="w")
            k += 1

        elif values[0] == "Дата СБКТС":
            ttk.Label(form_frame_tab1,text=  "Дата СБКТС", style="Custom.TLabel").grid(row=k, column=2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame_tab1, style="Custom.TEntry", width=34)
            entry.grid(row=k, column=3, padx=0, pady=5, sticky="w")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_sbcts"] = entry
            date_registration_button = ttk.Button(form_frame_tab1, width=14,  text="Выбрать дату",
                                                 command=lambda: date_time_selector.open_calendar(
                                                     entries_main["date_sbcts"], date_registration_button))
            date_registration_button.grid(row=k, column=3, padx=(216, 0), pady=5, sticky="w")
            k += 1

        elif values[0] == "Дата электронного ПТС":
            ttk.Label(form_frame_tab1,text=  "Дата электронного ПТС", style="Custom.TLabel").grid(row=k, column=2, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(form_frame_tab1, style="Custom.TEntry", width=34)
            entry.grid(row=k, column=3, padx=0, pady=5, sticky="w")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["epts_date"] = entry
            date_registration_button = ttk.Button(form_frame_tab1, width=14,  text="Выбрать дату",
                                                 command=lambda: date_time_selector.open_calendar(
                                                     entries_main["epts_date"], date_registration_button))
            date_registration_button.grid(row=k, column=3, padx=(216, 0), pady=5, sticky="w")
            k += 1

        elif values[0] == "Время предоставления ТС":
            ttk.Label(form_frame_tab1, text="Время предоставления ТС", style="Custom.TLabel").grid(row=k, column=2,
                                                                                                  padx=5, pady=5,
                                                                                                  sticky="e")
            entry = ttk.Entry(form_frame_tab1, style="Custom.TEntry", width=34)
            entry.grid(row=k, column=3, padx=0, pady=5, sticky="w")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["time_submission"] = entry
            time_registration_button = ttk.Button(form_frame_tab1, width=14, text="Выбрать время",
                                                 command=lambda: date_time_selector.open_time_selector(
                                                     entries_main["time_submission"], time_registration_button))
            time_registration_button.grid(row=k, column=3, padx=(216, 5), pady=5, sticky="w")
            k += 1

        elif values[2] == 'left':
            addElements.add_left_entry_info_ts (form_frame_tab1, values[0],  values[1],  i,  entries_main, 0, key)
            i += 1

        elif values[2] == 'right':
            addElements.add_right_entry_info_ts (form_frame_tab1, values[0],  values[1],  k,  entries_main, 2, key)
            k += 1

    # Сведения о документах, представленных для проведения оценки соответствия
    header_label_tab2 = ttk.Label(form_frame_tab1, text="Сведения о документах, представленных для проведения оценки соответствия", font=("Arial", 16, "bold"))
    header_label_tab2.grid(row=i, column=0, columnspan=4, pady=(15, 10), sticky="n")

    i += 1
    k = i

    # Создание элементов наличие документов
    for key, values in document_data.items():

        if values[2] == 'left':
            addElements.add_left_checkbox_info_ts(form_frame_tab1, values[0], values[1], i, checkbox_status, 0, key, checkbox_document)
            i += 1
        elif values[2] == 'right':
            addElements.add_right_checkbox_info_ts(form_frame_tab1, values[0], values[1], k, checkbox_status, 2, key, checkbox_document)
            k += 1

    # Условия окружающей среды
    header_label_tab2 = ttk.Label(form_frame_tab1, text="Условия окружающей среды", font=("Arial", 16, "bold"))
    header_label_tab2.grid(row=i, column=0, columnspan=4, pady=(15, 10), sticky="n")

    # Меняем индексы строк
    i+=1

    # Подзаголовок Бокс
    header_label_tab2 = ttk.Label(form_frame_tab1, text="Бокс", font=("Arial", 16, "bold"))
    header_label_tab2.grid(row=i, column=0, columnspan=2, pady=(15, 10), sticky="n")

    # Подзаголовок Улица
    header_label_tab2 = ttk.Label(form_frame_tab1, text="Площадка", font=("Arial", 16, "bold"))
    header_label_tab2.grid(row=i, column=2, columnspan=2, pady=(15, 10), sticky="n")

    # Меняем индексы строк
    i += 1
    k = i

    # Создание элементов условия ОС Бокс
    for key, values in environmental_data_box.items():

        if values[2] == 'left':
            addElements.add_left_entry_info_ts(form_frame_tab1, values[0], values[1], i, entries_e_box, 0, key)
            i += 1
        elif values[2] == 'right':
            addElements.add_right_entry_info_ts(form_frame_tab1, values[0], values[1], k, entries_e_box, 2, key)
            k += 1

    # Создание элементов условия ОС Улица
    for key, values in environmental_data_outside.items():

        if values[2] == 'left':
            addElements.add_left_entry_info_ts(form_frame_tab1, values[0], values[1], i, entries_e_outside, 0, key)
            i += 1
        elif values[2] == 'right':
            addElements.add_right_entry_info_ts(form_frame_tab1, values[0], values[1], k, entries_e_outside, 2, key)
            k += 1

    # Заголовок формы по центру
    header_label_tab2 = ttk.Label(form_frame_tab1, text="Информация о ТС", font=("Arial", 16, "bold"))
    header_label_tab2.grid(row=i, column=0, columnspan=4, pady=(15, 10), sticky="n")

    # Меняем индексы строк
    i +=1
    k = i

    # Создание элементов инфо о ТС
    for key, values in vehicle_data.items():

        if values[0] == "Марка транспортного средства":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Общие данные", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=10, sticky="n")
            i += 1
        elif values[0] == "- длина":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Габариты", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=10, sticky="n")
            i += 1
        elif values[0] == "Двигатель внутреннего сгорания (марка, тип)":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Двигатель внутреннего сгорания", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=10, sticky="n")
            k += 1
        elif values[0] == "- передняя":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Подвеска (тип)", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=10, sticky="n")
            i += 1
        elif values[0] == "- рабочая":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Тормозные системы (тип)", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=10, sticky="n")
            k += 1
        elif values[0] == "Электродвигатель электромобиля (марка, тип) 1":
            header_label_tab1 = ttk.Label(form_frame_tab1, text="Электрический двигатель", font=("Arial", 12, "bold"))
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=10, sticky="n")
            k += 1


        if values[2] == 'left':
            addElements.add_left_entry_info_ts (form_frame_tab1, values[0],  values[1],  i,  entries_ts, 0, key)
            i += 1
        elif values[2] == 'right':
            addElements.add_right_entry_info_ts (form_frame_tab1, values[0],  values[1],  k,  entries_ts, 2, key)
            k += 1

    save_button = tk.Button(form_frame_tab1, text="Редактировать", font=20, width=35, command=lambda: toggle_entries(id, entries_main, checkbox_status, entries_e_outside, entries_e_box,entries_ts, db_manager, save_button, checkbox_document))
    save_button.grid(row=i, column=0, columnspan=4, pady=(20,30), sticky="n")

def create_tab1(notebook, result, id, date_time_selector, addElements):
    # Создаем вкладку
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Общие данные")
    container_frame_tab1 = ttk.Frame(tab1)
    container_frame_tab1.pack(expand=True, fill="both", anchor="center", padx=4, pady=4)

    # Создаем форму
    form_frame_tab1 = ttk.Frame(container_frame_tab1)
    form_frame_tab1.pack(expand=True, fill="both", padx=0, pady=0)

    # Создаем словарь для хранения всех полей ввода
    entries_main = {}
    checkbox_status = {}
    checkbox_document = {}
    combobox_dict = {}

    form_frame_tab1.columnconfigure(0, weight=1)  # Левая колонка
    form_frame_tab1.columnconfigure(1, weight=1)  # Колонка между метками, занимает все доступное пространство
    form_frame_tab1.columnconfigure(2, weight=1)  # Правая колонка
    form_frame_tab1.columnconfigure(3, weight=1)  # Правая колонка

    # Словарь общие данные
    main_data = {
        "vin": ["Индификационный номер (VIN)", result.get('vin'), "left"],
        "customer": ["Заказчик", result.get('customer'), "left"],
        "owner": ["Собственник", result.get('owner'), "left"],
        "customer_address": ["Адрес заказчика", result.get('customer_address'), "left"],
        "actual_address": ["Фактический адрес (для юр. лиц)", result.get('actual_address'), "left"],
        "contact_phone": ["Контактный телефон", result.get('contact_phone'), "left"],
        "inn": ["ИНН", result.get('inn'), "left"],
        "kpp": ["КПП", result.get('kpp'), "left"],
        "ogrn": ["ОГРН/ОГРНИП", result.get('ogrn'), "left"],
        "email": ["ОГРН/ОГРНИП", result.get('email'), "left"],
        "delegate": ["Представитель заявителя (доверенное лицо)", result.get('delegate'), "left"],
        "identity_document": ["Документ, удостоверяющий личность представителя", result.get('identity_document'),
                              "left"],
        "power_of_attorney": ["Доверенность", result.get('power_of_attorney'), "left"],
        "dogovor": ["Договор (при наличии)", result.get('dogovor'), "right"],
        "date_registration": ["Дата оформления заявки", result.get('date_registration'), "right"],
        "date_submission": ["Дата предоставления ТС", result.get('date_submission'), "right"],
        "time_submission": ["Время предоставления ТС", result.get('time_submission'), "right"],
        "sbcts_num": ["Номер СБКТС", result.get('sbcts_num'), "right"],
        "date_sbcts": ["Дата СБКТС", result.get('date_sbcts'), "right"],
        "epts_num": ["Номер электронного ПТС", result.get('epts_num'), "right"],
        "epts_date": ["Дата электронного ПТС", result.get('epts_date'), "right"],
        "ets_num": ["Номер ETC", result.get('ets_num'), "right"],
        "status": ["Статус", result.get('status'), "right"]
    }

    # Предоставленные документы
    document_data = {
        "applicant_doc_1": ["Документ, удостоверяющий заявителя", result.get('applicant_doc_1'), "left"],
        "applicant_doc_2": ["Документ, подтверждающий право владения, или пользования и (или) распоряжения транспортным средством", result.get('applicant_doc_2'), "left"],
        "technical_description": ["Общее техническое описание транспортного средства", result.get('technical_description'), "left"],
        "doc_vin": ["Документ о присвоениии идентификационного номера транспортного средства (при наличии)", result.get('doc_vin'), "left"],
        "copies_of_certificates": ["Копии сертификатов на компоненты (при наличии)", result.get('copies_of_certificates'), "right"],
        "technical_documentation": ["Конструкторская, либо иная тех. документация по которой изготавливается продукция (при наличии)", result.get('technical_documentation'), "right"],
        "drawings": ["Чертежи оригинальных деталей и тех. карты их производства, либо соответ. эскизная док. (при наличии)", result.get('drawings'), "right"],
        "other_documents": ["Иная документация (при наличии)", result.get('other_documents'), "right"]
     }

    # Заголовок формы Общие данные
    header_label_tab1 = tk.Label(form_frame_tab1, text="Общие данные", font=("Arial", 16, "bold"),  width=18, height=2, borderwidth=2, relief="groove")
    header_label_tab1.grid(row=0, column=0, columnspan=4, pady=(0, 0), sticky="nsew")

    i = 1
    k = i

    # Создание элементов Общие данные
    for key, values in main_data.items():

        if values[0] == "Дата оформления заявки":
            # Создаем метку
            tk.Label(form_frame_tab1, text="Дата оформления заявки", borderwidth=2, relief="groove").grid(row=k,
                                                                                                        column=2,
                                                                                                          padx=0,
                                                                                                          pady=0,
                                                                                                          sticky="nsew")

            # Создаем фрейм-контейнер для поля ввода и кнопки
            container = tk.Frame(form_frame_tab1)
            container.grid(row=k, column=3, padx=1, pady=1, sticky="nsew")

            # Настройка контейнера для заполнения всей ячейки
            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            # Создаем поле ввода внутри контейнера
            entry = ttk.Entry(container, style="Custom.TEntry")
            entry.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_registration"] = entry

            # Создаем кнопку выбора даты внутри контейнера
            date_registration_button = ttk.Button(container, width=14, text="Выбрать дату",
                                                  command=lambda: date_time_selector.open_calendar(
                                                      entries_main["date_registration"], date_registration_button))
            date_registration_button.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="nsew")

            k += 1

        elif values[0] == "Дата предоставления ТС":
            tk.Label(form_frame_tab1, text="Дата предоставления ТС", borderwidth=2, relief="groove").grid(row=k,
                                                                                                          column=2,
                                                                                                          padx=0,
                                                                                                          pady=0,
                                                                                                          sticky="nsew")

            container = tk.Frame(form_frame_tab1)
            container.grid(row=k, column=3, padx=0, pady=0, sticky="nsew")

            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            entry = ttk.Entry(container, style="Custom.TEntry")
            entry.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_submission"] = entry

            date_submission_button = ttk.Button(container, width=14, text="Выбрать дату",
                                                command=lambda: date_time_selector.open_calendar(
                                                    entries_main["date_submission"], date_submission_button))
            date_submission_button.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="nsew")

            k += 1

        elif values[0] == "Дата СБКТС":
            tk.Label(form_frame_tab1, text="Дата СБКТС", borderwidth=2, relief="groove").grid(row=k, column=2, padx=0,
                                                                                              pady=0, sticky="nsew")

            container = tk.Frame(form_frame_tab1)
            container.grid(row=k, column=3, padx=0, pady=0, sticky="nsew")

            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            entry = ttk.Entry(container, style="Custom.TEntry")
            entry.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["date_sbcts"] = entry

            date_sbcts_button = ttk.Button(container, width=14, text="Выбрать дату",
                                           command=lambda: date_time_selector.open_calendar(
                                               entries_main["date_sbcts"], date_sbcts_button))
            date_sbcts_button.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="nsew")

            k += 1

        elif values[0] == "Дата электронного ПТС":
            tk.Label(form_frame_tab1, text="Дата электронного ПТС", borderwidth=2, relief="groove").grid(row=k,
                                                                                                         column=2,
                                                                                                         padx=0, pady=0,
                                                                                                         sticky="nsew")

            container = tk.Frame(form_frame_tab1)
            container.grid(row=k, column=3, padx=1, pady=1, sticky="nsew")

            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            entry = ttk.Entry(container, style="Custom.TEntry")
            entry.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["epts_date"] = entry

            epts_date_button = ttk.Button(container, width=14, text="Выбрать дату",
                                          command=lambda: date_time_selector.open_calendar(
                                              entries_main["epts_date"], epts_date_button))
            epts_date_button.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="nsew")

            k += 1

        elif values[0] == "Время предоставления ТС":
            tk.Label(form_frame_tab1, text="Время предоставления ТС", borderwidth=2, relief="groove").grid(row=k,
                                                                                                           column=2,
                                                                                                           padx=0,
                                                                                                           pady=0,
                                                                                                           sticky="nsew")
            container = tk.Frame(form_frame_tab1)
            container.grid(row=k, column=3, padx=1, pady=1, sticky="nsew")

            container.grid_columnconfigure(0, weight=1)
            container.grid_rowconfigure(0, weight=1)

            entry = ttk.Entry(container, style="Custom.TEntry")
            entry.grid(row=0, column=0, padx=(0, 0), pady=0, sticky="nsew")
            entry.insert(0, values[1] if values[1] else "")
            entries_main["time_submission"] = entry

            time_submission_button = ttk.Button(container, width=14, text="Выбрать время",
                                                command=lambda: date_time_selector.open_time_selector(
                                                    entries_main["time_submission"], time_submission_button))
            time_submission_button.grid(row=0, column=1, padx=(0, 0), pady=0, sticky="nsew")

            k += 1

        elif values[0] == "Статус":

            # Стиль для активного состояния
            style.configure("Custom.TCombobox",
                            fieldbackground="#f0f0f0",  # Цвет фона поля
                            background="#d3d3d3",  # Цвет фона выпадающего списка
                            foreground="black",  # Цвет текста
                            font=("Arial", 12))  # Шрифт

            # Настройка стиля для активного и неактивного состояний
            style.map("Custom.TCombobox",
                      fieldbackground=[('readonly', '#f0f0f0'), ('!disabled', '#ffffff')],
                      background=[('active', '#e0e0e0'), ('!active', '#d3d3d3')],
                      foreground=[('disabled', '#a0a0a0'), ('!disabled', 'black')])
            tk.Label(form_frame_tab1, text="Статус", borderwidth=2, relief="groove").grid(row=k,
                                                                                                           column=2,
                                                                                                           padx=0,
                                                                                                           pady=0,
                                                                                                           sticky="nsew")

            # Список значений для комбобокса
            options = ["На рассмотрении", "Произведено первичное оформление", "ТС представлено. В работе", "ТС представлено. Завершено",
                       "Оформлен СБКТС", "Оформлен ЭПТС", "Оформлен пакет ФГИС",  "Документы загружены во ФГИС",  "Архив"]
            # Создаем Combobox
            combobox = ttk.Combobox(form_frame_tab1, value = options, style="Custom.TCombobox")

            combobox.grid(row=k, column=3,  sticky="nsew")
            combobox.insert(0, values[1] if values[1] else "")
            combobox_dict["status"] =  combobox
            if result.get('status'):
                    combobox.set(result.get('status'))
            combobox.config(state="disable")
            k += 1

        elif values[2] == 'left':
            addElements.add_left_entry_info_ts (form_frame_tab1, values[0],  values[1],  i,  entries_main, 0, key, style)
            i += 1

        elif values[2] == 'right':
            addElements.add_right_entry_info_ts (form_frame_tab1, values[0],  values[1],  k,  entries_main, 2, key, style)
            k += 1

    # Сведения о документах, представленных для проведения оценки соответствия
    header_label_tab2 = tk.Label(form_frame_tab1, text="Сведения о документах, представленных для проведения оценки соответствия", font=("Arial", 16, "bold") ,
                                                                                                            width=80, height=2, borderwidth=2, relief="groove")
    header_label_tab2.grid(row=i, column=0, columnspan=4, pady=(0, 0), sticky="nsew")

    i += 1
    k = i

    # Создание элементов наличие документов
    for key, values in document_data.items():
        if values[2] == 'left':
           addElements.add_left_checkbox_info_ts(form_frame_tab1, values[0], values[1], i, checkbox_status, 0, key, checkbox_document)
           i += 1
        elif values[2] == 'right':
           addElements.add_right_checkbox_info_ts(form_frame_tab1, values[0], values[1], k, checkbox_status, 2, key, checkbox_document)
           k += 1

    style.configure("Custom.TButton", font=("Arial", 14))  # Задаем шрифт Arial размером 16

    # Применяем стиль к кнопке
    save_button = ttk.Button(form_frame_tab1, text="Редактировать", width=35, style="Custom.TButton",
                             command=lambda: toggle_entries(id, save_button, checkbox_document=checkbox_document, entries_main=entries_main, checkbox_status=checkbox_status, combobox_dict=combobox_dict))
    save_button.grid(row=i, column=0, columnspan=4, pady=20, sticky="n")

def create_tab2(notebook, result, id, addElements):
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Информация о ТС")

    # Создаем контейнерный фрейм для вкладки
    container_frame_tab2 = ttk.Frame(tab2)
    container_frame_tab2.pack(expand=True, fill="both", anchor="center", padx=4, pady=4)

    # Создаем форму
    form_frame_tab2 = addElements.create_scrollable_frame(container_frame_tab2)


    form_frame_tab2.columnconfigure(0, weight=1)  # Левая колонка
    form_frame_tab2.columnconfigure(1, weight=1)  # Колонка между метками, занимает все доступное пространство
    form_frame_tab2.columnconfigure(2, weight=1)  # Правая колонка
    form_frame_tab2.columnconfigure(3, weight=1)  # Правая колонка

    # Создаем словарь для хранения всех полей ввода
    entries_ts = {}


    # Словарь информация о ТС
    vehicle_data = {
        "brand": ["Марка транспортного средства", result.get('brand'), "left"],
        "model": ["Коммерческое наименование", result.get('model'), "left"],
        "type": ["Тип", result.get('type'), "left"],
        "chassis": ["Шасси транспортного средства", result.get('chassis'), "left"],
        "color": ["Цвет", result.get('color'), "left"],
        "year": ["Год выпуска", result.get('year'), "left"],
        "category": ["Категория транспортного средства", result.get('category'), "left"],
        "eco_class": ["Экологический класс", result.get('eco_class'), "left"],
        "manufacturer_address": ["Изготовитель транспортного средства", result.get('manufacturer_address'), "left"],
        "assembly_plant_address": ["Сборочный завод и его адрес", result.get('assembly_plant_address'), "left"],
        "wheel_formula": ["Колесная формула / ведущие колеса", result.get('wheel_formula'), "left"],
        "layout_scheme": ["Схема компоновки транспортного средства", result.get('layout_scheme'), "left"],
        "body_type": ["Тип кузова / количество дверей (для категории М1)", result.get('body_type'), "left"],
        "seating_capacity": ["Количество мест спереди / сзади (для категории М1)", result.get('seating_capacity'),
                             "left"],
        "izp": ["Исполнение загрузочного пространства (для категории N)", result.get('izp'), "left"],
        "cabin": ["Кабина (для категории N)", result.get('cabin'), "left"],
        "passenger_capacity": ["Пассажировместимость (для категорий М2, М3)", result.get('passenger_capacity'), "left"],
        "luggage_volume": ["Общий объем багажных отделений (для категории М3 класса III)", result.get('luggage_volume'),
                           "left"],
        "seating_capacity": ["Количество мест для сидения (для категорий М2, М3, L)", result.get('seating_capacity'),
                             "left"],
        "frame": ["Рама (для категории L)", result.get('frame'), "left"],
        "axes_count": ["Количество осей / колес (для категории О)", result.get('axes_count'), "left"],
        "vehicle_weight": ["Масса ТС в снаряженном состоянии, кг", result.get('vehicle_weight'),
                           "left"],
        "max_weight": ["Технически допустимая максимальная масса ТС, кг",
                       result.get('max_weight'), "left"],
        "length": ["- длина", result.get('length'), "left"],
        "width": ["- ширина", result.get('width'), "left"],
        "height": ["- высота", result.get('height'), "left"],
        "wheelbase": ["База, мм", result.get('wheelbase'), "left"],
        "track": ["Колея передних / задних колес, мм", result.get('track'), "left"],
        "hybrid": ["Описание гибридного транспортного средства", result.get('hybrid'), "left"],
        "front_suspension": ["- передняя", result.get('front_suspension'), "left"],
        "rear_suspension": ["- задняя", result.get('rear_suspension'), "left"],
        "engine": ["Двигатель внутреннего сгорания (марка, тип)", result.get('engine'), "right"],
        "cylinders": ["- количество и расположение цилиндров", result.get('cylinders'), "right"],
        "displacement": ["- рабочий объем цилиндров, см3", result.get('displacement'), "right"],
        "compression_ratio": ["- степень сжатия", result.get('compression_ratio'), "right"],
        "power": ["- максимальная мощность, кВт (мин – 1)", result.get('power'), "right"],
        "fuel": ["Топливо", result.get('fuel'), "right"],
        "fuel_system": ["Система питания (тип)", result.get('fuel_system'), "right"],
        "ignition_system": ["Система зажигания (тип)", result.get('power'), "right"],
        "exhaust_system": ["Система выпуска и нейтрализации отработавших газов", result.get('exhaust_system'), "right"],
        "e_engine_1": ["Электродвигатель электромобиля (марка, тип) 1", result.get('e_engine_1'), "right"],
        "voltage_1": ["Рабочее напряжение, В", result.get('voltage_1'), "right"],
        "max_30_power_1": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_1'), "right"],
        "e_engine_2": ["Электродвигатель электромобиля (марка, тип) 2", result.get('e_engine_2'), "right"],
        "voltage_2": ["Рабочее напряжение, В", result.get('voltage_2'), "right"],
        "max_30_power_2": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_2'), "right"],
        "energy_battery": ["Устройство накопления энергии (только для электромобилей)", result.get('energy_battery'),
                           "right"],
        "e_car": ["Электромашина: (марка, тип)", result.get('e_car'), "right"],
        "voltage": ["Рабочее напряжение, В", result.get('voltage'), "right"],
        "max_30_power": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power'), "right"],
        "clutch": ["Сцепление (марка, тип)", result.get('clutch'), "right"],
        "transmission": ["Трансмиссия", result.get('transmission'), "right"],
        "gearbox": ["Коробка передач (марка, тип)", result.get('gearbox'), "right"],
        "steering": ["Рулевое управление (марка, тип)", result.get('steering'), "right"],
        "working_brake": ["- рабочая", result.get('working_brake'), "right"],
        "spare_brake": ["-запасная", result.get('spare_brake'), "right"],
        "parking_brake": ["- стояночная", result.get('parking_brake'), "right"],
        "tires": ["Шины (обозначение размера)", result.get('tires'), "right"],
        "equipment": ["Дополнительное оборудование", result.get('equipment'), "right"]
    }

    # Заголовок формы Информаиця о ТС
    header_label_tab1 = tk.Label(form_frame_tab2, text="Информация о ТС", font=("Arial", 16, "bold"), width=25, height=2,
                                 borderwidth=2, relief="groove")
    header_label_tab1.grid(row=0, column=0, columnspan=4, pady=(0, 0), sticky="nswe")

    i = 1
    k = 1

    # Создание элементов инфо о ТС
    for key, values in vehicle_data.items():

        if values[0] == "Марка транспортного средства":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Общие данные", font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
            i += 1
        elif values[0] == "- длина":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Габариты", font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
            i += 1
        elif values[0] == "Двигатель внутреннего сгорания (марка, тип)":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Двигатель внутреннего сгорания",
                                          font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
            k += 1
        elif values[0] == "- передняя":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Подвеска (тип)", font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
            i += 1
        elif values[0] == "- рабочая":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Тормозные системы (тип)", font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
            k += 1
        elif values[0] == "Электродвигатель электромобиля (марка, тип) 1":
            header_label_tab1 = tk.Label(form_frame_tab2, text="Электрический двигатель", font=("Arial", 12, "bold"), relief="groove", height=2)
            header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
            k += 1

        if values[2] == 'left':
            addElements.add_left_entry_info_ts(form_frame_tab2, values[0], values[1], i, entries_ts, 0, key, style)
            i += 1
        elif values[2] == 'right':
            addElements.add_right_entry_info_ts(form_frame_tab2, values[0], values[1], k, entries_ts, 2, key, style)
            k += 1

    style.configure("Custom.TButton", font=("Arial", 14))  # Задаем шрифт Arial размером 16

    # Применяем стиль к кнопке
    save_button = ttk.Button(form_frame_tab2, text="Редактировать", width=35, style="Custom.TButton",
                             command=lambda: toggle_entries(id, save_button,  entries_ts=entries_ts))

    save_button.grid(row=i, column=0, columnspan=4, pady=20, sticky="n")

def create_tab4(notebook):
    # Создаем вкладку 5
    tab5 = ttk.Frame(notebook)
    notebook.add(tab5, text="Вкладка 5")
    # Добавьте нужные элементы и логику для этой вкладки

def open_details_window(tree):
    # Получаем выбранную строку
    selected_item = tree.selection()
    if selected_item:
        item_data = tree.item(selected_item, 'values')
        application_id = item_data[1]  # ID заявки

        # Создаем экземпляр класса DateTimeSelector
        date_time_selector = DateTimeSelector(root)
        addElements = AddElements(root)

        # Выполняем запрос к базе данных для получения данных заявки
        result = db_manager.fetch_application_data(application_id)

        if not result:
            return  # Если данные не найдены или произошла ошибка, выходим из функции

        # Создаем новое окно
        details_window = tk.Toplevel()
        details_window.title(f"Детали заявки ID: {item_data[0]}")
        details_window.geometry("1440x900")

        # Создаем объект Notebook (вкладки)
        notebook = ttk.Notebook(details_window)

        # Блокируем доступ к другим окнам
        #details_window.grab_set()

        # Создаем вкладки с помощью отдельных функций
        create_tab1(notebook, result, application_id, date_time_selector, addElements)
        create_tab2(notebook, result, application_id, addElements)
        #create_tab3(notebook)
        #create_tab4(notebook)

        notebook.pack(expand=True, fill="both")

        # Ожидание закрытия окна
        details_window.wait_window()


# Функция для скрытия всех фреймов
def hide_all_frames():
    application_frame.pack_forget()
    sbcts_archive_frame.pack_forget()
    settings_frame.pack_forget()

# Функция для изменения контента правой области
def change_content(content):
    hide_all_frames()  # Скрываем все фреймы перед показом нужного

    if  content == "Список заявок":
        application_frame.pack(fill="both", expand=True)
    elif content == "Архив заявок":
        archive_frame.pack(fill="both", expand=True)
    elif content == "Поиск СБКТС":
        sbcts_archive_frame.pack(fill="both", expand=True)
    elif content == "Настройки":
        settings_frame.pack(fill="both", expand=True)


# Список заявок
def create_application_frame(application_frame, data=None, page=0, id_value='', vin_value='', model_value='', brand_value='', owner_value='', date_app_value='', date_archive_value=''):

    # Количество элементов на странице
    items_per_page = 50
    start = page * items_per_page
    end = start + items_per_page


    # Очищаем фрейм
    for widget in application_frame.winfo_children():
        widget.destroy()
        print('s')

    # Настройка колонок и строк
    for i in range(8):
        application_frame.columnconfigure(i, weight=1)

    application_frame.rowconfigure(2, weight=1)  # Позволяем Treeview расширяться


    # Фильтры и поля ввода
    id_label = tk.Label(application_frame, text="ID", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"),
                         borderwidth=2, relief="groove")
    id_label.grid(row=0, column=0, padx=2, pady=(2, 2), sticky="nsew")
    id_entry = ttk.Entry(application_frame, font=("Arial", 13))
    id_entry.grid(row=1, column=0, padx=2, pady=(2, 2), sticky="nsew")
    id_entry.insert(0, id_value)  # Вставляем текущее значение VIN

    vin_label = tk.Label(application_frame, text="VIN", font=("Arial", 12), bg=application_frame.cget("bg"),
                           borderwidth=2, relief="groove")
    vin_label.grid(row=0, column=1, padx=2, pady=(2, 2), sticky="nsew")
    vin_entry = ttk.Entry(application_frame, font=("Arial", 13))
    vin_entry.grid(row=1, column=1, padx=2, pady=(2, 2), sticky="nsew")
    vin_entry.insert(0, vin_value)  # Вставляем текущее значение модели

    model_label = tk.Label(application_frame, text="Модель", font=("Arial", 12), bg=application_frame.cget("bg"),
                           borderwidth=2, relief="groove")
    model_label.grid(row=0, column=2, padx=2, pady=(2, 2), sticky="nsew")
    model_entry = ttk.Entry(application_frame, font=("Arial", 13))
    model_entry.grid(row=1, column=2, padx=2, pady=(2, 2), sticky="nsew")
    model_entry.insert(0, model_value)  # Вставляем текущее значение бренда

    brand_label = tk.Label(application_frame, text="Марка", font=("Arial", 12), bg=application_frame.cget("bg"),
                          borderwidth=2, relief="groove")
    brand_label.grid(row=0, column=3, padx=2, pady=(2, 2), sticky="nsew")
    brand_entry = ttk.Entry(application_frame, font=("Arial", 13))
    brand_entry.grid(row=1, column=3, padx=2, pady=(2, 2), sticky="nsew")
    brand_entry.insert(0, brand_value)  # Вставляем текущее значение типа

    owner_label = tk.Label(application_frame, text="Собственник", font=("Arial", 12),
                            bg=application_frame.cget("bg"), borderwidth=2, relief="groove")
    owner_label.grid(row=0, column=4, padx=2, pady=(2, 2), sticky="nsew")
    owner_entry = ttk.Entry(application_frame, font=("Arial", 13))
    owner_entry.grid(row=1, column=4, padx=2, pady=(2, 2), sticky="nsew")
    owner_entry.insert(0, owner_value)  # Вставляем текущее значение двигателя




    # Кнопка Поиск
    def search_data():
        nonlocal data  # Объявляем, что используем внешнюю переменную data
        id_value = id_entry.get()
        vin_value = vin_entry.get()
        model_value = model_entry.get()
        brand_value = brand_entry.get()
        owner_value = owner_entry.get()
        date_app_value = date_app_entry.get()
        date_archive_value = date_archive_entry.get()



        # Получаем данные из базы данных
        data = db_manager.fetch_data_application_archive(id_value, vin_value, model_value, brand_value, owner_value, date_app_value, date_archive_value)
        # Передаем введенные значения обратно в create_sbcts_archive_frame
        create_application_frame(application_frame, data, 0, id_value, vin_value, model_value, brand_value,
                                   owner_value, date_app_value, date_archive_value)

    search_button = ttk.Button(application_frame, text="Поиск", command=search_data)
    search_button.grid(row=0, column=7, padx=2, pady=(2, 2), sticky="nsew")

    # Кнопка Сброс
    def reset_search():
        create_sbcts_archive_frame(application_frame, None, 0)

    reset_button = ttk.Button(application_frame, text="Сброс", command=reset_search)
    reset_button.grid(row=1, column=7, padx=2, pady=(2, 2), sticky="nsew")

    # Создание Treeview для таблицы
    columns = ("№", "ID", "VIN", "Марка", "Модель", "Заказчик", "Собственник","Дата заявки", "Дата арихивации")
    tree = ttk.Treeview(application_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        if col == "№":
            tree.column(col, width=30, anchor="center", stretch=False)
        if col == "ID":
            tree.column(col, width=30, anchor="center", stretch=False)
        if col == "VIN":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Марка":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Модель":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Заказчик":
            tree.column(col, width=120, anchor="w", stretch=True)
        if col == "Собственник":
            tree.column(col, width=120, anchor="w", stretch=True)
        if col == "Дата заявки":
            tree.column(col, width=150, anchor="w", stretch=False)
        if col == "Дата арихивации":
            tree.column(col, width=150, anchor="w", stretch=False)

    if data:
        # Добавление данных в Treeview
        for index, row in enumerate(data[start:end], start=start + 1):  # Нумерация начинается с start + 1
            tree.insert("", tk.END, values=(index,) + row)  # Добавляем номер как первый элемент

    # Добавление Scrollbar
    scrollbar = ttk.Scrollbar(application_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=2, column=0, columnspan=8, sticky="nsew")
    scrollbar.grid(row=2, column=8, sticky="ns")

    # Пагинация
    def next_page():
        if (page + 1) * items_per_page < len(data):
            create_sbcts_archive_frame(application_frame, data, page + 1, vin_value, model_value, brand_value,
                                       type_value, engine_value)

    def previous_page():
        if page > 0:
            create_sbcts_archive_frame(application_frame, data, page - 1, vin_value, model_value, brand_value,
                                       type_value, engine_value)

    # Кнопки для перехода на следующую и предыдущую страницу
    prev_button = ttk.Button(application_frame, text="Предыдущая страница", command=previous_page)
    prev_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    next_button = ttk.Button(application_frame, text="Следующая страница", command=next_page)
    next_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # Привязываем внешний обработчик события
    tree.bind("<Double-1>", lambda event: open_details_window(tree))

    date_app_label = tk.Label(application_frame, text="Дата заявки", font=("Arial", 12),
                              bg=application_frame.cget("bg"), borderwidth=2, relief="groove", width=20)
    date_app_label.grid(row=0, column=5, padx=2, pady=(2, 2), sticky="nsew")
    date_app_entry = DateEntry(application_frame, borderwidth=2, date_pattern="yyyy-mm-dd", relief="groove")
    date_app_entry.configure(validate='none')
    date_app_entry.grid(row=1, column=5, padx=2, pady=(2, 2), sticky="nsew")

    if date_app_value:
        date_app_entry.set_date(date_app_value)
    else:
        date_app_entry.delete(0, tk.END)

    date_archive_label = tk.Label(application_frame, text="Дата архивации", font=("Arial", 12),
                                  bg=application_frame.cget("bg"), borderwidth=2, relief="groove", width=20)
    date_archive_label.grid(row=0, column=6, padx=2, pady=(2, 2), sticky="nsew")
    date_archive_entry = DateEntry(application_frame, borderwidth=2, date_pattern="yyyy-mm-dd", relief="groove")
    date_archive_entry.configure(validate='none')
    date_archive_entry.grid(row=1, column=6, padx=2, pady=(2, 2), sticky="nsew")

    if date_archive_value:
        date_archive_entry.set_date(date_archive_value)
    else:
        date_archive_entry.delete(0, tk.END)



# Функция для открытия формы в новом окне
def open_create_form():
    create_window = tk.Toplevel(root)
    create_window.title("Создание заявки")
    create_window.geometry("750x600")
    create_window.grab_set()  # Блокируем главное окно, пока новое окно активно

    # Создаем экземпляр класса DateTimeSelector
    date_time_selector = DateTimeSelector(root)

    # Блокируем изменение размеров окна
    create_window.resizable(False, False)

    # Стили для Label и Entry
    label_style = {"font": ("Arial", 12)}
    entry_style = {"font": ("Arial", 12), "bd": 1, "relief": "solid", "width": 40}

    # Настройка растяжения колонок
    create_window.grid_columnconfigure(0, weight=1)
    create_window.grid_columnconfigure(1, weight=1)

    # Заголовок формы
    label = tk.Label(create_window, text="Создание заявки", font=("Arial", 20))
    label.grid(row=0, column=0, columnspan=2, pady=(10, 10))

    # Фрейм для элементов формы
    form_frame = tk.Frame(create_window)
    form_frame.grid(row=1, column=0, columnspan=2, pady=(20, 0))

    # Поле ввода для VIN номера
    vin_label = tk.Label(form_frame, text="VIN номер:", **label_style)
    vin_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
    vin_entry = tk.Entry(form_frame, **entry_style)
    vin_entry.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="ew")

    # Поле ввода для Марки ТС
    brand_label = tk.Label(form_frame, text="Марка:", **label_style)
    brand_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    brand_entry = tk.Entry(form_frame, **entry_style)
    brand_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    # Поле ввода для Модели ТС
    model_label = tk.Label(form_frame, text="Модель:", **label_style)
    model_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    model_entry = tk.Entry(form_frame, **entry_style)
    model_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # Поле ввода для Типа двигателя
    dvs_label = tk.Label(form_frame, text="Тип двигателя:", **label_style)
    dvs_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    dvs_entry = tk.Entry(form_frame, **entry_style)
    dvs_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    # Поле ввода для Цвета ТС
    color_label = tk.Label(form_frame, text="Цвет:", **label_style)
    color_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
    color_entry = tk.Entry(form_frame, **entry_style)
    color_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

    # Поле ввода для ФИО собственника
    fio_label = tk.Label(form_frame, text="ФИО собственника:", **label_style)
    fio_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
    fio_entry = tk.Entry(form_frame, **entry_style)
    fio_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    # Поле ввода для Заказчика
    customer_label = tk.Label(form_frame, text="Заказчик:", **label_style)
    customer_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
    customer_entry = tk.Entry(form_frame, **entry_style)
    customer_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

    # Поле для отображения выбранной даты предоставления ТС
    date_label = tk.Label(form_frame, text="Дата предоставления ТС:", **label_style)
    date_label.grid(row=9, column=0, padx=10, pady=5, sticky="e")
    date_entry = tk.Entry(form_frame, **entry_style)
    date_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

    # Кнопка для вызова календаря
    date_button = tk.Button(form_frame, text="Выбрать дату", width=14, font=("Arial", 8),
                            command=lambda: date_time_selector.open_calendar(date_entry, date_button))
    date_button.grid(row=9, column=2, padx=(0, 10), pady=5, sticky="ew")

    # Поле ввода для Времени предоставления ТС
    time_label = tk.Label(form_frame, text="Время предоставления ТС:", **label_style)
    time_label.grid(row=10, column=0, padx=10, pady=5, sticky="e")
    time_entry = tk.Entry(form_frame, **entry_style)
    time_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

    # Кнопка для выбора времени
    time_button = tk.Button(form_frame, text="Выбрать время", width=14, font=("Arial", 8),
                            command=lambda: date_time_selector.open_time_selector(time_entry, time_button))
    time_button.grid(row=10, column=2, padx=(0, 10), pady=5, sticky="e")

    # Поле для отображения даты оформления заявки
    date_provision_label = tk.Label(form_frame, text="Дата оформления заявки:", **label_style)
    date_provision_label.grid(row=11, column=0, padx=10, pady=5, sticky="e")
    date_provision_entry = tk.Entry(form_frame, **entry_style)
    date_provision_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")

    # Кнопка для вызова календаря для даты оформления заявки
    date_provision_button = tk.Button(form_frame, text="Выбрать дату", width=14, font=("Arial", 8),
                                      command=lambda: date_time_selector.open_calendar(date_provision_entry, date_provision_button))
    date_provision_button.grid(row=11, column=2, padx=(0, 10), pady=5, sticky="w")

    # Кнопка для подтверждения заявки
    submit_button = tk.Button(create_window, text="Создать заявку", font=("Arial", 12),
                              command=lambda: db_manager.submit_form(vin_entry.get(), fio_entry.get(),
                                                          brand_entry.get(), model_entry.get(),
                                                          dvs_entry.get(), color_entry.get(),
                                                          customer_entry.get(),
                                                          date_entry.get(), time_entry.get(),
                                                          date_provision_entry.get(), create_window))
    submit_button.grid(row=12, column=0, columnspan=2, pady=(50, 10), sticky="n")


# Создать фрейм Архив СБКТС
def create_sbcts_archive_frame(sbcts_archive_frame, data=None, page=0, vin_value='', model_value='', brand_value='', type_value='', engine_value='', var_char_value  = False):



    # Количество элементов на странице
    items_per_page = 50
    start = page * items_per_page
    end = start + items_per_page

    # Очищаем фрейм
    for widget in sbcts_archive_frame.winfo_children():
        widget.destroy()

    # Настройка колонок и строк
    for i in range(6):
        sbcts_archive_frame.columnconfigure(i, weight=1)

    sbcts_archive_frame.rowconfigure(2, weight=1)  # Позволяем Treeview расширяться

    # Фильтры и поля ввода
    vin_label = tk.Label(sbcts_archive_frame, text="VIN", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"), borderwidth=2, relief="groove")
    vin_label.grid(row=0, column=0, padx=2, pady=(2, 2), sticky="nsew")
    vin_entry = ttk.Entry(sbcts_archive_frame, font=("Arial", 12))
    vin_entry.grid(row=1, column=0, padx=2, pady=(2, 2), sticky="nsew")
    vin_entry.insert(0, vin_value)  # Вставляем текущее значение VIN

    model_label = tk.Label(sbcts_archive_frame, text="Модель", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"), borderwidth=2, relief="groove")
    model_label.grid(row=0, column=1, padx=2, pady=(2, 2), sticky="nsew")
    model_entry = ttk.Entry(sbcts_archive_frame, font=("Arial", 13))
    model_entry.grid(row=1, column=1, padx=2, pady=(2, 2), sticky="nsew")
    model_entry.insert(0, model_value)  # Вставляем текущее значение модели

    brand_label = tk.Label(sbcts_archive_frame, text="Марка", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"), borderwidth=2, relief="groove")
    brand_label.grid(row=0, column=2, padx=2, pady=(2, 2), sticky="nsew")
    brand_entry = ttk.Entry(sbcts_archive_frame, font=("Arial", 13))
    brand_entry.grid(row=1, column=2, padx=2, pady=(2, 2), sticky="nsew")
    brand_entry.insert(0, brand_value)  # Вставляем текущее значение бренда

    type_label = tk.Label(sbcts_archive_frame, text="Тип", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"), borderwidth=2, relief="groove")
    type_label.grid(row=0, column=3, padx=2, pady=(2, 2), sticky="nsew")
    type_entry = ttk.Entry(sbcts_archive_frame, font=("Arial", 13))
    type_entry.grid(row=1, column=3, padx=2, pady=(2, 2), sticky="nsew")
    type_entry.insert(0, type_value)  # Вставляем текущее значение типа

    engine_label = tk.Label(sbcts_archive_frame, text="Двигатель", font=("Arial", 12), bg=sbcts_archive_frame.cget("bg"), borderwidth=2, relief="groove")
    engine_label.grid(row=0, column=4, padx=2, pady=(2, 2), sticky="nsew")
    engine_entry = ttk.Entry(sbcts_archive_frame, font=("Arial", 13))
    engine_entry.grid(row=1, column=4, padx=2, pady=(2, 2), sticky="nsew")
    engine_entry.insert(0, engine_value)  # Вставляем текущее значение двигателя

    # Кнопка Поиск
    def search_data():
        nonlocal data  # Объявляем, что используем внешнюю переменную data
        vin_value = vin_entry.get()
        model_value = model_entry.get()
        brand_value = brand_entry.get()
        type_value = type_entry.get()
        engine_value = engine_entry.get()
        var_char_value = check_var.get()

        # Получаем данные из базы данных
        data = db_manager.fetch_data_sbcts_archive(vin_value, brand_value, model_value, type_value, engine_value,var_char_value )
        # Передаем введенные значения обратно в create_sbcts_archive_frame
        create_sbcts_archive_frame(sbcts_archive_frame, data, 0, vin_value, model_value, brand_value, type_value, engine_value, var_char_value)

    search_button = ttk.Button(sbcts_archive_frame, text="Поиск", command=search_data)
    search_button.grid(row=0, column=5, padx=2, pady=(2, 2), sticky="nsew")

    # Кнопка Сброс
    def reset_search():
        create_sbcts_archive_frame(sbcts_archive_frame, None, 0)

    reset_button = ttk.Button(sbcts_archive_frame, text="Сброс", command=reset_search)
    reset_button.grid(row=1, column=5, padx=2, pady=(2, 2), sticky="nsew")

    # Создание Treeview для таблицы
    columns = ("№", "VIN", "Марка", "Модель", "Тип", "Двигатель", "Номер СБКТС")
    tree = ttk.Treeview(sbcts_archive_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        if col == "№":
            tree.column(col, width=30, anchor="center", stretch=False)
        if col == "VIN":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Марка":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Модель":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Тип":
            tree.column(col, width=70, anchor="w", stretch=True)
        if col == "Двигатель":
            tree.column(col, width=120, anchor="w", stretch=True)
        if col == "Номер СБКТС":
            tree.column(col, width=50, anchor="w", stretch=True)

    if data:
        # Добавление данных в Treeview
        for index, row in enumerate(data[start:end], start=start + 1):  # Нумерация начинается с start + 1
            tree.insert("", tk.END, values=(index,) + row)  # Добавляем номер как первый элемент

    # Добавление Scrollbar
    scrollbar = ttk.Scrollbar(sbcts_archive_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.grid(row=2, column=0, columnspan=6, sticky="nsew")
    scrollbar.grid(row=2, column=6, sticky="ns")

    # Пагинация
    def next_page():
        if (page + 1) * items_per_page < len(data):
            create_sbcts_archive_frame(sbcts_archive_frame, data, page + 1, vin_value, model_value, brand_value, type_value, engine_value)

    def previous_page():
        if page > 0:
            create_sbcts_archive_frame(sbcts_archive_frame, data, page - 1, vin_value, model_value, brand_value, type_value, engine_value)

    # Кнопки для перехода на следующую и предыдущую страницу
    prev_button = ttk.Button(sbcts_archive_frame, text="Предыдущая страница", command=previous_page)
    prev_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    next_button = ttk.Button(sbcts_archive_frame, text="Следующая страница", command=next_page)
    next_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    check_var = tk.BooleanVar()
    checkbutton = tk.Checkbutton(sbcts_archive_frame, text="Только наша ИЛ", variable=check_var,  borderwidth=2, relief="groove")
    checkbutton.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
    check_var.set(var_char_value)

    # Привязываем внешний обработчик события
    tree.bind("<Double-1>", lambda event: on_item_select(tree))
# Создать фрейм Архив СБКТС, подробная информация
def on_item_select(tree):
    # Получаем выбранную строку
    selected_item = tree.selection()
    if selected_item:
        addElements = AddElements(root)

        item_data = tree.item(selected_item, 'values')

        # Выполняем запрос к базе данных для получения данных заявки
        result = db_manager.fetch_sbcts_data_archive(item_data[6])

        if not result:
            return

        create_window = tk.Toplevel(root)
        create_window.title(item_data[6])
        create_window.geometry("1440x900")

        # Создаем контейнерный фрейм внутри create_window, как в примере с tab2
        container_frame = ttk.Frame(create_window)
        container_frame.pack(expand=True, fill="both", anchor="center", padx=4, pady=4)

        # Создаем прокручиваемый фрейм внутри контейнерного фрейма
        scrollable_frame = addElements.create_scrollable_frame(container_frame)
        scrollable_frame.pack(expand=True, fill="both", padx=4, pady=4)



        # Настройка растяжения колонок
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)
        scrollable_frame.grid_columnconfigure(2, weight=1)
        scrollable_frame.grid_columnconfigure(3, weight=1)

        # Создаем словарь для хранения всех полей ввода
        entries_ts = {}

        # Словарь информация о ТС
        vehicle_data = {
            "brand": ["Марка транспортного средства", result.get('brand'), "left"],
            "model": ["Коммерческое наименование", result.get('model'), "left"],
            "type": ["Тип", result.get('type'), "left"],
            "chassis": ["Шасси транспортного средства", result.get('chassis'), "left"],
            "color": ["Цвет", result.get('color'), "left"],
            "year": ["Год выпуска", result.get('year'), "left"],
            "category": ["Категория транспортного средства", result.get('category'), "left"],
            "eco_class": ["Экологический класс", result.get('eco_class'), "left"],
            "manufacturer_address": ["Изготовитель транспортного средства", result.get('manufacturer_address'), "left"],
            "assembly_plant_address": ["Сборочный завод и его адрес", result.get('assembly_plant_address'), "left"],
            "wheel_formula": ["Колесная формула / ведущие колеса", result.get('wheel_formula'), "left"],
            "layout_scheme": ["Схема компоновки транспортного средства", result.get('layout_scheme'), "left"],
            "body_type": ["Тип кузова / количество дверей (для категории М1)", result.get('body_type'), "left"],
            "seating_capacity": ["Количество мест спереди / сзади (для категории М1)", result.get('seating_capacity'),
                                 "left"],
            "izp": ["Исполнение загрузочного пространства (для категории N)", result.get('izp'), "left"],
            "cabin": ["Кабина (для категории N)", result.get('cabin'), "left"],
            "passenger_capacity": ["Пассажировместимость (для категорий М2, М3)", result.get('passenger_capacity'),
                                   "left"],
            "luggage_volume": ["Общий объем багажных отделений (для категории М3 класса III)",
                               result.get('luggage_volume'),
                               "left"],
            "seating_capacity": ["Количество мест для сидения (для категорий М2, М3, L)",
                                 result.get('seating_capacity'),
                                 "left"],
            "frame": ["Рама (для категории L)", result.get('frame'), "left"],
            "axes_count": ["Количество осей / колес (для категории О)", result.get('axes_count'), "left"],
            "vehicle_weight": ["Масса ТС в снаряженном состоянии, кг", result.get('vehicle_weight'),
                               "left"],
            "max_weight": ["Технически допустимая максимальная масса ТС, кг",
                           result.get('max_weight'), "left"],
            "length": ["- длина", result.get('length'), "left"],
            "width": ["- ширина", result.get('width'), "left"],
            "height": ["- высота", result.get('height'), "left"],
            "wheelbase": ["База, мм", result.get('wheelbase'), "left"],
            "track": ["Колея передних / задних колес, мм", result.get('track'), "left"],
            "hybrid": ["Описание гибридного транспортного средства", result.get('hybrid'), "left"],
            "front_suspension": ["- передняя", result.get('front_suspension'), "left"],
            "rear_suspension": ["- задняя", result.get('rear_suspension'), "left"],
            "engine": ["Двигатель внутреннего сгорания (марка, тип)", result.get('engine'), "right"],
            "cylinders": ["- количество и расположение цилиндров", result.get('cylinders'), "right"],
            "displacement": ["- рабочий объем цилиндров, см3", result.get('displacement'), "right"],
            "compression_ratio": ["- степень сжатия", result.get('compression_ratio'), "right"],
            "power": ["- максимальная мощность, кВт (мин – 1)", result.get('power'), "right"],
            "fuel": ["Топливо", result.get('fuel'), "right"],
            "fuel_system": ["Система питания (тип)", result.get('fuel_system'), "right"],
            "ignition_system": ["Система зажигания (тип)", result.get('power'), "right"],
            "exhaust_system": ["Система выпуска и нейтрализации отработавших газов", result.get('exhaust_system'),
                               "right"],
            "e_engine_1": ["Электродвигатель электромобиля (марка, тип) 1", result.get('e_engine_1'), "right"],
            "voltage_1": ["Рабочее напряжение, В", result.get('voltage_1'), "right"],
            "max_30_power_1": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_1'), "right"],
            "e_engine_2": ["Электродвигатель электромобиля (марка, тип) 2", result.get('e_engine_2'), "right"],
            "voltage_2": ["Рабочее напряжение, В", result.get('voltage_2'), "right"],
            "max_30_power_2": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power_2'), "right"],
            "energy_battery": ["Устройство накопления энергии (только для электромобилей)",
                               result.get('energy_battery'),
                               "right"],
            "e_car": ["Электромашина: (марка, тип)", result.get('e_car'), "right"],
            "voltage": ["Рабочее напряжение, В", result.get('voltage'), "right"],
            "max_30_power": ["Максимальная 30-минутная мощность, кВт", result.get('max_30_power'), "right"],
            "clutch": ["Сцепление (марка, тип)", result.get('clutch'), "right"],
            "transmission": ["Трансмиссия", result.get('transmission'), "right"],
            "gearbox": ["Коробка передач (марка, тип)", result.get('gearbox'), "right"],
            "steering": ["Рулевое управление (марка, тип)", result.get('steering'), "right"],
            "working_brake": ["- рабочая", result.get('working_brake'), "right"],
            "spare_brake": ["-запасная", result.get('spare_brake'), "right"],
            "parking_brake": ["- стояночная", result.get('parking_brake'), "right"],
            "tires": ["Шины (обозначение размера)", result.get('tires'), "right"],
            "equipment": ["Дополнительное оборудование", result.get('equipment'), "right"]
        }

        # Заголовок номер документа
        doc_num_label = tk.Label(scrollable_frame, text=result.get('number'), font=("Arial", 14, "bold"),
                                     borderwidth=2, relief="groove")
        doc_num_label.grid(row=0, column=0, pady=(0, 0), sticky="nswe")

        # Заголовок вмн номер
        vin_label = tk.Label(scrollable_frame, text=result.get('vin'), font=("Arial", 14, "bold"),
                                 borderwidth=2, relief="groove")
        vin_label.grid(row=0, column=1, pady=(0, 0), sticky="nswe")

        style.configure("Custom.TButton", font=("Arial", 14))  # Задаем шрифт Arial размером 16

        # Применяем стиль к кнопке
        load_button = ttk.Button(scrollable_frame, text="Открыть документ", style = "Custom.TButton",
                                 command=lambda: load_application_list(result))
        load_button.grid(row=0, column=2, pady = 1, padx= 1, sticky="nswe")

        # Применяем стиль к кнопке
        open_button = ttk.Button(scrollable_frame, text="Загрузить данные", style = "Custom.TButton",
                                 command=lambda: load_application_list(result))

        open_button.grid(row=0, column=3, pady=1, padx=1, sticky="nswe")


        # Заголовок формы Информаиця о ТС
        header_label_tab1 = tk.Label(scrollable_frame, text="Информация о ТС", font=("Arial", 16, "bold"), width=25,
                                     borderwidth=2, relief="groove")
        header_label_tab1.grid(row=1, column=0, columnspan=4, pady=(0, 0), sticky="nswe")

        i = 2
        k = 2


        # Создание элементов инфо о ТС
        for key, values in vehicle_data.items():

            if values[0] == "Марка транспортного средства":
                header_label_tab1 = tk.Label(scrollable_frame, text="Общие данные", font=("Arial", 12, "bold"),
                                             relief="groove", height=2)
                header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
                i += 1
            elif values[0] == "- длина":
                header_label_tab1 = tk.Label(scrollable_frame, text="Габариты", font=("Arial", 12, "bold"),
                                             relief="groove", height=2)
                header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
                i += 1
            elif values[0] == "Двигатель внутреннего сгорания (марка, тип)":
                header_label_tab1 = tk.Label(scrollable_frame, text="Двигатель внутреннего сгорания",
                                             font=("Arial", 12, "bold"), relief="groove", height=2)
                header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
                k += 1
            elif values[0] == "- передняя":
                header_label_tab1 = tk.Label(scrollable_frame, text="Подвеска (тип)", font=("Arial", 12, "bold"),
                                             relief="groove", height=2)
                header_label_tab1.grid(row=i, column=0, columnspan=2, pady=0, sticky="nswe")
                i += 1
            elif values[0] == "- рабочая":
                header_label_tab1 = tk.Label(scrollable_frame, text="Тормозные системы (тип)",
                                             font=("Arial", 12, "bold"), relief="groove", height=2)
                header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
                k += 1
            elif values[0] == "Электродвигатель электромобиля (марка, тип) 1":
                header_label_tab1 = tk.Label(scrollable_frame, text="Электрический двигатель",
                                             font=("Arial", 12, "bold"), relief="groove", height=2)
                header_label_tab1.grid(row=k, column=2, columnspan=2, pady=0, sticky="nswe")
                k += 1

            if values[2] == 'left':
                addElements.add_left_entry_info_ts(scrollable_frame, values[0], values[1], i, entries_ts, 0, key, style)
                i += 1
            elif values[2] == 'right':
                addElements.add_right_entry_info_ts(scrollable_frame, values[0], values[1], k, entries_ts, 2, key, style)
                k += 1

# Выбрать заявку для загрузки шаблона из СБКТС
def load_application_list(ts_info):
    # Третье окно
    create_window = tk.Toplevel(root)
    create_window.title("Выбор заявки")
    create_window.geometry("800x600")

    # Запрет на изменение размера окна
    create_window.resizable(False, False)

    # Блокировка других окон
    create_window.grab_set()

    # Создание Treeview для таблицы
    columns = ("ID", "VIN", "Марка", "Модель")
    tree = ttk.Treeview(create_window, columns=columns, show="headings")

    data = db_manager.get_unfinished_application()

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=70, anchor="w", stretch=True)

    for row in data:
        tree.insert("", "end", values=row)

    # Заголовок для выбора
    head_label = tk.Label(create_window, text="Выберите документ для загрузки данных", font=("Arial", 14, "bold"),
                          borderwidth=2, relief="groove")
    head_label.grid(row=0, column=0, pady=(0, 0), sticky="nswe")

    # Добавление Scrollbar
    scrollbar = ttk.Scrollbar(create_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.grid(row=1, column=0, sticky="nsew")
    scrollbar.grid(row=1, column=1, sticky="ns")

    create_window.grid_rowconfigure(1, weight=1)
    create_window.grid_columnconfigure(0, weight=1)
    create_window.grid_columnconfigure(1, weight=0)

    # Функция для обработки клика по элементу в Treeview
    def on_item_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            values = item['values']

            # Функции для обработки выбора "Да" и "Нет"
            def on_yes():
                db_manager.load_data_info_ts(values[0], ts_info)


                create_window.destroy()


            def on_no():
                print("Пользователь выбрал 'Нет'")

            # Открываем окно с подтверждением
            create_confirmation_window(create_window,f"Загрузить данные в заявку с VIN {values[0]}",
                                       on_yes, on_no)

    # Привязка события на выбор элемента в Treeview
    tree.bind("<Double-1>", on_item_select)

    # Блокировка главного окна
    create_window.grab_set()

# Окно выбора Да / нет
def create_confirmation_window(parent_window, message, on_yes, on_no):
    # Создаем новое окно поверх родительского
    confirm_window = tk.Toplevel(parent_window)
    confirm_window.title("Подтверждение")
    confirm_window.geometry("300x120")
    confirm_window.resizable(False, False)

    # Размещаем окно над родительским
    confirm_window.transient(parent_window)
    confirm_window.grab_set()  # Блокировка родительского окна

    # Сообщение с подтверждением
    message_label = tk.Label(confirm_window, text=message, wraplength=244, font=("Arial", 12))
    message_label.pack(pady=10)

    # Фрейм для кнопок "Да" и "Нет"
    button_frame = tk.Frame(confirm_window)
    button_frame.pack(pady=10)

    # Кнопка "Да"
    yes_button = ttk.Button(button_frame, text="Да", width=10, command=lambda: [on_yes(), confirm_window.destroy()])
    yes_button.grid(row=0, column=0, padx=10)

    # Кнопка "Нет"
    no_button = ttk.Button(button_frame, text="Нет", width=10, command=lambda: [on_no(), confirm_window.destroy()])
    no_button.grid(row=0, column=1, padx=10)

    # Центрирование окна относительно родительского
    parent_window.update_idletasks()  # Обновляем размеры окон
    x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - (confirm_window.winfo_width() // 2)
    y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - (confirm_window.winfo_height() // 2)
    confirm_window.geometry(f'+{x}+{y}')

    # Ожидание закрытия окна
    confirm_window.wait_window()


def create_settings_frame():
    # Пример: можно здесь настроить содержимое для настроек
    label = tk.Label(settings_frame, text="Настройки", **label_style)
    label.pack()


 # Сделать поля и чекбоксы редактируемыми/нередактируемыми
def toggle_entries(id,save_button, entries_main=None, checkbox_status=None, entries_e_outside=None, entries_e_box=None, entries_ts=None,checkbox_document=None, combobox_dict=None):


    # Настройка стиля для неактивного Entry
    style.configure("Disabled.TEntry",  fieldbackground="#e0e0e0", font=("Arial", 11))

    # Настройка стиля для активного Entry
    style.configure("Enable.TEntry",  fieldbackground="#FFFFFF", font=("Arial", 11))


    # Определяем новое состояние на основе имени кнопки
    if save_button['text'] == "Редактировать":
        save_button.config(text='Сохранить')

        if entries_main:
            for entry in entries_main.values():
                entry.config(state="enable", style="Enable.TEntry")

        if entries_ts:
            for entry in entries_ts.values():
                entry.config(state="enable", style="Enable.TEntry")

        if checkbox_document:
            for checkbox in checkbox_document.values():
                checkbox.config(state="enable")

        if combobox_dict:
            for combobox in combobox_dict.values():
                combobox.config(state="enable")





    elif save_button['text'] == "Сохранить":
        save_button.config(text='Редактировать')

        if entries_main:
            for entry in entries_main.values():
                entry.config(state="readonly", style="Disabled.TEntry")
            db_manager.change_data_main(id=id, entries_main=entries_main, checkbox_status=checkbox_status, combobox_dict=combobox_dict)

        if entries_ts:
            for entry in entries_ts.values():
                entry.config(state="readonly", style="Disabled.TEntry")
            db_manager.change_data_main(id=id, entries_ts=entries_ts)

        if checkbox_document:
            for checkbox in checkbox_document.values():
                checkbox.config(state="disabled")

        if combobox_dict:
            for combobox in combobox_dict.values():
                combobox.config(state="disabled")


    else:

        return None # Ничего не делаем, если имя кнопки не соответствует



# Создание фреймов
create_application_frame(application_frame)
create_sbcts_archive_frame(sbcts_archive_frame)
create_settings_frame()











# Запуск приложения
if __name__ == "__main__":
    root.mainloop()
