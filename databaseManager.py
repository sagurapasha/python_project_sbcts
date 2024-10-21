import psycopg2
from tkinter import messagebox, ttk
from datetime import datetime
from tkinter import messagebox
import psycopg2.extras
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_host, db_name_1, db_name_2, db_user, db_password):
        self.db_host = db_host
        self.db_name_1 = db_name_1
        self.db_name_2 = db_name_2
        self.db_user = db_user
        self.db_password = db_password
    # Функция для удаления табуляций, новых строк, боковых пробелов

    def clean_input(self, value):
        if value is not None:
            return value.strip(" \n\r\t") if value.strip(" \n\r\t") else None
        return None

    # Функция для проверки даты
    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    # Проверка формата времени
    def validate_time(self, time_text):
        try:
            # Сначала пытаемся распознать время в формате '%H:%M'
            datetime.strptime(time_text, '%H:%M')
            return True
        except ValueError:
            try:
                # Если первый формат не подходит, пробуем формат '%H:%M:%S'
                datetime.strptime(time_text, '%H:%M:%S')
                return True
            except ValueError:
                # Если оба формата не подходят, возвращаем False
                return False

    # Соединение с базой данных
    def connect(self):
        try:
            connection = psycopg2.connect(
                host=self.db_host,
                database=self.db_name_1,
                user=self.db_user,
                password=self.db_password
            )
            return connection
        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {error}")
            return None

    # Соединение с базой данных
    def connect_2(self):
        try:
            connection = psycopg2.connect(
                host=self.db_host,
                database=self.db_name_2,
                user=self.db_user,
                password=self.db_password
            )
            return connection
        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {error}")
            return None

    # Внесение первичных данных в таблицу (оформления заявки)
    def submit_form(self, vin, fio, brand, model, dvs, color, customer, date, time_with_seconds, date_provision, create_window):
        connection = self.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()

            # Проверяем дату и время подачи заявки
            if date and not self.validate_date(date):
                messagebox.showerror("Ошибка", "Неверный формат даты. Ожидается формат: ГГГГ-ММ-ДД.")
                return

            if time_with_seconds and not self.validate_time(time_with_seconds):
                messagebox.showerror("Ошибка", "Неверный формат времени. Ожидается формат: ЧЧ:ММ.")
                return

            # Проверяем дату регистрации
            if date_provision and not self.validate_date(date_provision):
                messagebox.showerror("Ошибка", "Неверный формат даты регистрации. Ожидается формат: ГГГГ-ММ-ДД.")
                return



            vin = self.clean_input(vin)
            fio = self.clean_input(fio)
            customer = self.clean_input(customer)
            date = self.clean_input(date)
            date_provision = self.clean_input(date_provision)
            brand = self.clean_input(brand)
            model = self.clean_input(model)
            dvs = self.clean_input(dvs)
            color = self.clean_input(color)


            # Заменяем пустые строки на None для обработки как NULL в базе данных
            vin = vin if vin else None
            fio = fio if fio else None
            customer = customer if customer else None
            date = date if date else None
            date_provision = date_provision if date_provision else None
            brand = brand if brand else None
            model = model if model else None
            dvs = dvs if dvs else None
            color = color if color else None
            time_with_seconds = time_with_seconds if time_with_seconds else None

            # SQL-запрос для вставки данных
            insert_query = """
            INSERT INTO application (owner, customer, date_submission, time_submission, date_registration)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """
            cursor.execute(insert_query, (vin, fio, customer, date, time_with_seconds, date_provision))
            new_id = cursor.fetchone()[0]

            update_query = """
            UPDATE ts_info SET brand = %s, model = %s, fuel = %s, color = %s, vin = %s WHERE id = %s
            """
            cursor.execute(update_query, (brand, model, dvs, color, vin, new_id))

            connection.commit()
            messagebox.showinfo("Успех", "Заявка успешно добавлена в базу данных!")
            create_window.destroy()

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка BD", f"Ошибка при добавлении записи: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Получение полных данных для таблицы заявок
    def fetch_data(self):
        connection = self.connect()
        if connection is None:
            return []

        try:
            cursor = connection.cursor()
            fetch_query = """
            SELECT application.id, application.date_registration, application.date_submission, ts_info.vin, ts_info.brand, ts_info.model,
                   application.customer, application.owner, application.status
            FROM application
            JOIN ts_info ON application.id = ts_info.id
            """
            cursor.execute(fetch_query)
            rows = cursor.fetchall()
            return rows

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка при извлечении данных: {error}")
            return []
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Фильтрации таблицы заявок
    def search_data(self, id_value, vin_value, customer_value, date_value, date_provision_value, tree):
        connection = self.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            base_query = """
            SELECT application.id, application.date_registration, application.date_submission, ts_info.vin, ts_info.brand, ts_info.model,
                   application.customer, application.owner, application.status
            FROM application
            JOIN ts_info ON application.id = ts_info.id
            WHERE 1=1
            """

            filters = []
            if id_value:
                filters.append(f"AND application.id = {id_value}")
            if vin_value:
                filters.append(f"AND ts_info.vin ILIKE '%{vin_value}%'")
            if customer_value:
                filters.append(f"AND application.customer ILIKE '%{customer_value}%'")
            if date_value:
                filters.append(f"AND application.date_submission = '{date_value}'")
            if date_provision_value:
                filters.append(f"AND application.date_registration = '{date_provision_value}'")

            final_query = base_query + " ".join(filters)


            cursor.execute(final_query)
            rows = cursor.fetchall()

            # Очищаем таблицу перед обновлением
            for item in tree.get_children():
                tree.delete(item)

            # Заполняем таблицу новыми данными
            for row in rows:
                tree.insert("", "end", values=row)

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка при фильтрации данных: {error}")
        finally:
            if connection:
                cursor.close()
                connection.close()

    # Получение полных данных из трех таблиц (Заявки)
    def fetch_application_data(self, application_id):
        """
        Выполняет SQL-запрос для получения данных из таблиц application, ts_info и environmental_conditions
        по указанному ID заявки.
        Возвращает результат запроса.
        """
        connection = self.connect()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # SQL-запрос для получения данных из трех таблиц
            query = f"""
            SELECT *
            FROM application
            JOIN ts_info ON application.id = ts_info.id
            JOIN measurement ON application.id = measurement.id
            WHERE application.id = {application_id};
            """
            cursor.execute(query)
            result = cursor.fetchone()

            cursor.close()
            return result

        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {error}")
            return None
        finally:
            if connection:
                connection.close()

    # Получение  данных о ТС из архива СБКТС
    def fetch_sbcts_data_archive(self, number):
        """
        Выполняет SQL-запрос для получения данных из таблиц application, ts_info и environmental_conditions
        по указанному ID заявки.
        Возвращает результат запроса.
        """
        connection = self.connect_2()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # SQL-запрос для получения данных из трех таблиц
            query = f"SELECT * FROM sbkts WHERE number = '{number}'"

            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            return result

        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {error}")
            return None
        finally:
            if connection:
                connection.close()

    # Изменение общий данных в заявках
    def change_data_main(self, id, entries_main = None, checkbox_status=None,entries_ts=None, combobox_dict=None):

        connection = self.connect()
        if connection is None:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных.")
            return None
        try:

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            if entries_main:
                # Общие данные
                vin = entries_main['vin'].get() if entries_main['vin'].get() else None
                customer = entries_main['customer'].get() if entries_main['customer'].get() else None
                owner = entries_main['owner'].get() if entries_main['owner'].get() else None
                date_registration = entries_main['date_registration'].get()
                date_submission = entries_main['date_submission'].get()
                time_submission = entries_main['time_submission'].get()
                status = combobox_dict['status'].get() if combobox_dict['status'].get() else None
                sbcts_num = entries_main['sbcts_num'].get() if entries_main['sbcts_num'].get() else None
                epts_num = entries_main['epts_num'].get() if entries_main['epts_num'].get() else None
                customer_address = entries_main['customer_address'].get() if entries_main['customer_address'].get() else None
                actual_address = entries_main['actual_address'].get() if entries_main['actual_address'].get() else None
                contact_phone = entries_main['contact_phone'].get() if entries_main['contact_phone'].get() else None
                inn = entries_main['inn'].get() if entries_main['inn'].get() else None
                kpp = entries_main['kpp'].get() if entries_main['kpp'].get() else None
                email = entries_main['email'].get() if entries_main['email'].get() else None
                ogrn = entries_main['ogrn'].get() if entries_main['ogrn'].get() else None
                delegate = entries_main['delegate'].get() if entries_main['delegate'].get() else None
                identity_document = entries_main['identity_document'].get() if entries_main['identity_document'].get() else None
                power_of_attorney = entries_main['power_of_attorney'].get() if entries_main['power_of_attorney'].get() else None
                dogovor = entries_main['dogovor'].get() if entries_main['dogovor'].get() else None
                ets_num = entries_main['ets_num'].get() if entries_main['ets_num'].get() else None
                date_sbcts = entries_main['date_sbcts'].get() if entries_main['date_sbcts'].get() else None
                epts_date = entries_main['epts_date'].get() if entries_main['epts_date'].get() else None
                date_registration = entries_main['date_registration'].get() if entries_main['date_registration'].get() else None
                date_submission = entries_main['date_submission'].get() if entries_main['date_submission'].get() else None
                time_submission = entries_main['time_submission'].get() if entries_main['time_submission'].get() else None
                date_sbcts = entries_main['date_sbcts'].get() if entries_main['date_sbcts'].get() else None
                epts_date = entries_main['epts_date'].get() if entries_main['epts_date'].get() else None

                # Наличие документов
                applicant_doc_1 = checkbox_status['applicant_doc_1'].get()
                applicant_doc_2 = checkbox_status['applicant_doc_2'].get()
                technical_description = checkbox_status['technical_description'].get()
                doc_vin = checkbox_status['doc_vin'].get()
                copies_of_certificates = checkbox_status['copies_of_certificates'].get()
                technical_documentation = checkbox_status['technical_documentation'].get()
                drawings = checkbox_status['drawings'].get()
                other_documents = checkbox_status['other_documents'].get()

                # Проверяем дату подачи заявки
                if date_registration and not self.validate_date(date_registration):
                    messagebox.showerror("Ошибка", "Неверный формат даты. Ожидается формат: ГГГГ-ММ-ДД.")
                    return

                # Проверяем дату предоставления
                if date_submission and not self.validate_date(date_submission):
                    messagebox.showerror("Ошибка", "Неверный формат даты регистрации. Ожидается формат: ГГГГ-ММ-ДД.")
                    return

                # Проверяем время предоставления
                if time_submission and not self.validate_time(time_submission):
                    messagebox.showerror("Ошибка", "Неверный формат времени. Ожидается формат: ЧЧ:ММ.")
                    return

                # Проверяем дату СБКТС
                if date_sbcts and not self.validate_date(date_sbcts):
                    messagebox.showerror("Ошибка", "Неверный формат даты СБКТС. Ожидается формат: ГГГГ-ММ-ДД.")
                    return

                # Проверяем дату ЕПТС
                if epts_date and not self.validate_date(epts_date):
                    messagebox.showerror("Ошибка", "Неверный формат даты ЕПТС. Ожидается формат: ГГГГ-ММ-ДД.")
                    return

                # Создание запрос
                query_main = """
                    UPDATE application 
                    SET 
                        customer = %s, 
                        owner = %s, 
                        date_registration = %s, 
                        date_submission = %s, 
                        time_submission = %s, 
                        status = %s, 
                        sbcts_num = %s, 
                        date_sbcts = %s, 
                        epts_num = %s, 
                        epts_date = %s, 
                        customer_address = %s, 
                        actual_address = %s, 
                        contact_phone = %s, 
                        inn = %s, 
                        kpp = %s, 
                        email = %s, 
                        ogrn = %s, 
                        delegate = %s, 
                        identity_document = %s, 
                        power_of_attorney = %s, 
                        dogovor = %s, 
                        ets_num = %s, 
                        applicant_doc_1 = %s, 
                        applicant_doc_2 = %s, 
                        technical_description = %s, 
                        doc_vin = %s, 
                        copies_of_certificates = %s, 
                        technical_documentation = %s, 
                        drawings = %s, 
                        other_documents = %s 
                    WHERE id = %s
                """

                query_vin = f"UPDATE ts_info SET vin = '{vin}' WHERE id = {id}"

                values_main = (customer, owner, date_registration, date_submission, time_submission, status,
                    sbcts_num, date_sbcts, epts_num, epts_date, customer_address, actual_address, contact_phone,
                    inn, kpp, email, ogrn, delegate, identity_document, power_of_attorney, dogovor, ets_num,
                    applicant_doc_1, applicant_doc_2, technical_description, doc_vin, copies_of_certificates,
                    technical_documentation, drawings, other_documents, id)

                cursor.execute(query_vin)

                cursor.execute(query_main, values_main)

            elif entries_ts:
                # Данные о ТС
                brand = entries_ts['brand'].get() if entries_ts['brand'].get() else None
                model = entries_ts['model'].get() if entries_ts['model'].get() else None
                type = entries_ts['type'].get() if entries_ts['type'].get() else None
                chassis = entries_ts['chassis'].get() if entries_ts['chassis'].get() else None
                year = entries_ts['year'].get() if entries_ts['year'].get() else None
                category = entries_ts['category'].get() if entries_ts['category'].get() else None
                eco_class = entries_ts['eco_class'].get() if entries_ts['eco_class'].get() else None
                manufacturer_address = entries_ts['manufacturer_address'].get() if entries_ts['manufacturer_address'].get() else None
                assembly_plant_address = entries_ts['assembly_plant_address'].get() if entries_ts['assembly_plant_address'].get() else None
                wheel_formula = entries_ts['wheel_formula'].get() if entries_ts['wheel_formula'].get() else None
                vehicle_weight = entries_ts['vehicle_weight'].get() if entries_ts['vehicle_weight'].get() else None
                max_weight = entries_ts['max_weight'].get() if entries_ts['max_weight'].get() else None
                cylinders = entries_ts['cylinders'].get() if entries_ts['cylinders'].get() else None
                length = entries_ts['length'].get() if entries_ts['length'].get() else None
                width = entries_ts['width'].get() if entries_ts['width'].get() else None
                height = entries_ts['height'].get() if entries_ts['height'].get() else None
                wheelbase = entries_ts['wheelbase'].get() if entries_ts['wheelbase'].get() else None
                track = entries_ts['track'].get() if entries_ts['track'].get() else None
                engine = entries_ts['engine'].get() if entries_ts['engine'].get() else None
                voltage = entries_ts['voltage'].get() if entries_ts['voltage'].get() else None
                displacement = entries_ts['displacement'].get() if entries_ts['displacement'].get() else None
                compression_ratio = entries_ts['compression_ratio'].get() if entries_ts['compression_ratio'].get() else None
                power = entries_ts['power'].get() if entries_ts['power'].get() else None
                fuel = entries_ts['fuel'].get() if entries_ts['fuel'].get() else None
                passenger_capacity = entries_ts['passenger_capacity'].get() if entries_ts['passenger_capacity'].get() else None
                fuel_system = entries_ts['fuel_system'].get() if entries_ts['fuel_system'].get() else None
                ignition_system = entries_ts['ignition_system'].get() if entries_ts['ignition_system'].get() else None
                gearbox = entries_ts['gearbox'].get() if entries_ts['gearbox'].get() else None
                front_suspension = entries_ts['front_suspension'].get() if entries_ts['front_suspension'].get() else None
                rear_suspension = entries_ts['rear_suspension'].get() if entries_ts['rear_suspension'].get() else None
                steering = entries_ts['steering'].get() if entries_ts['steering'].get() else None
                working_brake = entries_ts['working_brake'].get() if entries_ts['working_brake'].get() else None
                spare_brake = entries_ts['spare_brake'].get() if entries_ts['spare_brake'].get() else None
                parking_brake = entries_ts['parking_brake'].get() if entries_ts['parking_brake'].get() else None
                equipment = entries_ts['equipment'].get() if entries_ts['equipment'].get() else None
                exhaust_system = entries_ts['exhaust_system'].get() if entries_ts['exhaust_system'].get() else None
                energy_battery = entries_ts['energy_battery'].get() if entries_ts['energy_battery'].get() else None
                transmission = entries_ts['transmission'].get() if entries_ts['transmission'].get() else None
                e_car = entries_ts['e_car'].get() if entries_ts['e_car'].get() else None
                max_30_power = entries_ts['max_30_power'].get() if entries_ts['max_30_power'].get() else None
                layout_scheme = entries_ts['layout_scheme'].get() if entries_ts['layout_scheme'].get() else None
                seating_capacity = entries_ts['seating_capacity'].get() if entries_ts['seating_capacity'].get() else None
                body_type = entries_ts['body_type'].get() if entries_ts['body_type'].get() else None
                frame = entries_ts['frame'].get() if entries_ts['frame'].get() else None
                tires = entries_ts['tires'].get() if entries_ts['tires'].get() else None
                axes_count = entries_ts['axes_count'].get() if entries_ts['axes_count'].get() else None
                hybrid = entries_ts['hybrid'].get() if entries_ts['hybrid'].get() else None
                color = entries_ts['color'].get() if entries_ts['color'].get() else None
                izp = entries_ts['izp'].get() if entries_ts['izp'].get() else None
                cabin = entries_ts['cabin'].get() if entries_ts['cabin'].get() else None
                e_engine_1 = entries_ts['e_engine_1'].get() if entries_ts['e_engine_1'].get() else None
                voltage_1 = entries_ts['voltage_1'].get() if entries_ts['voltage_1'].get() else None
                max_30_power_1 = entries_ts['max_30_power_1'].get() if entries_ts['max_30_power_1'].get() else None
                max_30_power_2 = entries_ts['max_30_power_2'].get() if entries_ts['max_30_power_2'].get() else None
                e_engine_2 = entries_ts['e_engine_2'].get() if entries_ts['e_engine_2'].get() else None
                voltage_2 = entries_ts['voltage_2'].get() if entries_ts['voltage_2'].get() else None
                luggage_volume = entries_ts['luggage_volume'].get() if entries_ts['luggage_volume'].get() else None
                clutch = entries_ts['clutch'].get() if entries_ts['clutch'].get() else None

# Создание запроса
                query_ts = """
                    UPDATE public.ts_info
                    SET brand = %s,
                        model = %s,
                        type = %s,
                        chassis = %s,
                        year = %s,
                        category = %s,
                        eco_class = %s,
                        manufacturer_address = %s,
                        assembly_plant_address = %s,
                        wheel_formula = %s,
                        vehicle_weight = %s,
                        max_weight = %s,
                        length = %s,
                        width = %s,
                        height = %s,
                        wheelbase = %s,
                        track = %s,
                        engine = %s,
                        cylinders = %s,
                        displacement = %s,
                        compression_ratio = %s,
                        power = %s,
                        fuel = %s,
                        fuel_system = %s,
                        ignition_system = %s,
                        gearbox = %s,
                        front_suspension = %s,
                        rear_suspension = %s,
                        steering = %s,
                        working_brake = %s,
                        spare_brake = %s,
                        parking_brake = %s,
                        equipment = %s,
                        exhaust_system = %s,
                        energy_battery = %s,
                        transmission = %s,
                        e_car = %s,
                        voltage = %s,
                        max_30_power = %s,
                        layout_scheme = %s,
                        seating_capacity = %s,
                        body_type = %s,
                        frame = %s,
                        tires = %s,
                        axes_count = %s,
                        passenger_capacity = %s,
                        hybrid = %s,
                        color = %s,
                        izp = %s,
                        cabin = %s,
                        e_engine_1 = %s,
                        voltage_1 = %s,
                        max_30_power_1 = %s,
                        e_engine_2 = %s,
                        voltage_2 = %s,
                        max_30_power_2 = %s,
                        luggage_volume = %s,
                        clutch = %s
                    WHERE id = %s
                """

                values_ts = (brand, model, type, chassis, year, category, eco_class,
                    manufacturer_address, assembly_plant_address, wheel_formula, vehicle_weight, max_weight, length, width,
                    height, wheelbase, track, engine, cylinders, displacement, compression_ratio, power, fuel,
                    fuel_system, ignition_system, gearbox, front_suspension, rear_suspension,
                    steering, working_brake, spare_brake, parking_brake, equipment, exhaust_system, energy_battery,
                    transmission, e_car, voltage, max_30_power, layout_scheme, seating_capacity, body_type,
                    frame, tires, axes_count, passenger_capacity, hybrid, color, izp, cabin, e_engine_1,
                    voltage_1, max_30_power_1, e_engine_2, voltage_2, max_30_power_2, luggage_volume, clutch, id)

                cursor.execute(query_ts, values_ts)

            connection.commit()

        except ValueError as ve:
            messagebox.showerror("Ошибка", str(ve))
            print(str(ve))
            return None
        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {error}")
            print(error)
            return None
        finally:
            if connection:
                connection.close()


    def get_unfinished_application(self):
        connection = self.connect()
        if connection is None:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных.")
            return None
        try:

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            query = "SELECT application.id, vin, brand, model  FROM application INNER JOIN ts_info ON application.id = ts_info.id WHERE status != 'Архив'"
            cursor.execute(query)

            result              = cursor.fetchall()

            connection.commit()

            return   result

        except ValueError as ve:
            messagebox.showerror("Ошибка", str(ve))
            print(str(ve))
            return None
        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {error}")
            print(error)
            return None
        finally:
            if connection:
                connection.close()


    def load_data_info_ts(self, id, entries_ts):
        connection = self.connect()

        if connection is None:
            messagebox.showerror("Ошибка", "Нет подключения к базе данных.")
            return None
        try:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            # Данные о ТС
            brand = entries_ts['brand'].replace("\n", " ") if entries_ts['brand'] else None
            model = entries_ts['model'].replace("\n", " ") if entries_ts['model'] else None
            type = entries_ts['type'].replace("\n", " ") if entries_ts['type']else None
            chassis = entries_ts['chassis'].replace("\n", " ") if entries_ts['chassis'] else None
            year = entries_ts['year'].replace("\n", " ") if entries_ts['year'] else None
            category = entries_ts['category'].replace("\n", " ") if entries_ts['category'] else None
            eco_class = entries_ts['eco_class'].replace("\n", " ") if entries_ts['eco_class'] else None
            manufacturer_address = entries_ts['manufacturer_address'].replace("\n", " ") if entries_ts[
                'manufacturer_address'] else None
            assembly_plant_address = entries_ts['assembly_plant_address'].replace("\n", " ") if entries_ts[
                'assembly_plant_address'] else None
            wheel_formula = entries_ts['wheel_formula'].replace("\n", " ") if entries_ts['wheel_formula'] else None
            vehicle_weight = entries_ts['vehicle_weight'] .replace("\n", " ")if entries_ts['vehicle_weight'] else None
            max_weight = entries_ts['max_weight'].replace("\n", " ") if entries_ts['max_weight'] else None
            cylinders = entries_ts['cylinders'].replace("\n", " ") if entries_ts['cylinders'] else None
            length = entries_ts['length'].replace("\n", " ") if entries_ts['length'] else None
            width = entries_ts['width'].replace("\n", " ") if entries_ts['width'] else None
            height = entries_ts['height'].replace("\n", " ") if entries_ts['height'] else None
            wheelbase = entries_ts['wheelbase'].replace("\n", " ") if entries_ts['wheelbase'] else None
            track = entries_ts['track'].replace("\n", " ") if entries_ts['track'] else None
            engine = entries_ts['engine'].replace("\n", " ") if entries_ts['engine'] else None
            # voltage = entries_ts['voltage'] if entries_ts['voltage'] else None
            displacement = entries_ts['displacement'].replace("\n", " ") if entries_ts['displacement'] else None
            compression_ratio = entries_ts['compression_ratio'].replace("\n", " ") if entries_ts['compression_ratio'] else None
            power = entries_ts['power'].replace("\n", " ") if entries_ts['power'] else None
            fuel = entries_ts['fuel'].replace("\n", " ") if entries_ts['fuel'] else None
            passenger_capacity = entries_ts['passenger_capacity'].replace("\n", " ") if entries_ts[
                'passenger_capacity'] else None
            fuel_system = entries_ts['fuel_system'].replace("\n", " ") if entries_ts['fuel_system'] else None
            ignition_system = entries_ts['ignition_system'].replace("\n", " ") if entries_ts['ignition_system'] else None
            gearbox = entries_ts['gearbox'].replace("\n", " ") if entries_ts['gearbox'] else None
            front_suspension = entries_ts['front_suspension'].replace("\n", " ") if entries_ts['front_suspension'] else None
            rear_suspension = entries_ts['rear_suspension'].replace("\n", " ") if entries_ts['rear_suspension'] else None
            steering = entries_ts['steering'].replace("\n", " ") if entries_ts['steering'] else None
            working_brake = entries_ts['working_brake'].replace("\n", " ") if entries_ts['working_brake'] else None
            spare_brake = entries_ts['spare_brake'].replace("\n", " ") if entries_ts['spare_brake'] else None
            parking_brake = entries_ts['parking_brake'].replace("\n", " ") if entries_ts['parking_brake'] else None
            equipment = entries_ts['equipment'].replace("\n", " ") if entries_ts['equipment'] else None
            exhaust_system = entries_ts['exhaust_system'].replace("\n", " ")if entries_ts['exhaust_system'] else None
            energy_battery = entries_ts['energy_battery'].replace("\n", " ") if entries_ts['energy_battery'] else None
            transmission = entries_ts['transmission'].replace("\n", " ") if entries_ts['transmission'] else None
            e_car = entries_ts['e_car'].replace("\n", " ") if entries_ts['e_car'] else None
            # max_30_power = entries_ts['max_30_power'] if entries_ts['max_30_power'] else None
            layout_scheme = entries_ts['layout_scheme'].replace("\n", " ") if entries_ts['layout_scheme'] else None
            seating_capacity = entries_ts['seating_capacity'].replace("\n", " ") if entries_ts['seating_capacity'] else None
            body_type = entries_ts['body_type'].replace("\n", " ") if entries_ts['body_type'] else None
            frame = entries_ts['frame'].replace("\n", " ") if entries_ts['frame'] else None
            tires = entries_ts['tires'].replace("\n", " ") if entries_ts['tires'] else None
            axes_count = entries_ts['axes_count'].replace("\n", " ") if entries_ts['axes_count'] else None
            hybrid = entries_ts['hybrid'] .replace("\n", " ")if entries_ts['hybrid'] else None
            # color = entries_ts['color'] if entries_ts['color'] else None
            izp = entries_ts['izp'].replace("\n", " ") if entries_ts['izp'] else None
            cabin = entries_ts['cabin'].replace("\n", " ") if entries_ts['cabin'] else None
            e_engine_1 = entries_ts['e_engine_1'].replace("\n", " ") if entries_ts['e_engine_1'] else None
            voltage_1 = entries_ts['voltage_1'].replace("\n", " ") if entries_ts['voltage_1'] else None
            max_30_power_1 = entries_ts['max_30_power_1'].replace("\n", " ") if entries_ts['max_30_power_1'] else None
            max_30_power_2 = entries_ts['max_30_power_2'].replace("\n", " ") if entries_ts['max_30_power_2'] else None
            e_engine_2 = entries_ts['e_engine_2'].replace("\n", " ") if entries_ts['e_engine_2'] else None
            voltage_2 = entries_ts['voltage_2'].replace("\n", " ") if entries_ts['voltage_2'] else None
            luggage_volume = entries_ts['luggage_volume'].replace("\n", " ") if entries_ts['luggage_volume'] else None
            # clutch = entries_ts['clutch'] if entries_ts['clutch'] else None

            # Создание запроса
            query_ts = """
                                UPDATE public.ts_info
                                SET brand = %s,
                                    model = %s,
                                    type = %s,
                                    chassis = %s,
                                    year = %s,
                                    category = %s,
                                    eco_class = %s,
                                    manufacturer_address = %s,
                                    assembly_plant_address = %s,
                                    wheel_formula = %s,
                                    vehicle_weight = %s,
                                    max_weight = %s,
                                    length = %s,
                                    width = %s,
                                    height = %s,
                                    wheelbase = %s,
                                    track = %s,
                                    engine = %s,
                                    cylinders = %s,
                                    displacement = %s,
                                    compression_ratio = %s,
                                    power = %s,
                                    fuel = %s,
                                    fuel_system = %s,
                                    ignition_system = %s,
                                    gearbox = %s,
                                    front_suspension = %s,
                                    rear_suspension = %s,
                                    steering = %s,
                                    working_brake = %s,
                                    spare_brake = %s,
                                    parking_brake = %s,
                                    equipment = %s,
                                    exhaust_system = %s,
                                    energy_battery = %s,
                                    transmission = %s,
                                    e_car = %s,
                                    layout_scheme = %s,
                                    seating_capacity = %s,
                                    body_type = %s,
                                    frame = %s,
                                    tires = %s,
                                    axes_count = %s,
                                    passenger_capacity = %s,
                                    hybrid = %s,
                                    izp = %s,
                                    cabin = %s,
                                    e_engine_1 = %s,
                                    voltage_1 = %s,
                                    max_30_power_1 = %s,
                                    e_engine_2 = %s,
                                    voltage_2 = %s,
                                    max_30_power_2 = %s,
                                    luggage_volume = %s
                                WHERE id = %s
                            """

            values_ts = (brand, model, type, chassis, year, category, eco_class,
                         manufacturer_address, assembly_plant_address, wheel_formula, vehicle_weight, max_weight,
                         length, width,
                         height, wheelbase, track, engine, cylinders, displacement, compression_ratio, power, fuel,
                         fuel_system, ignition_system, gearbox, front_suspension, rear_suspension,
                         steering, working_brake, spare_brake, parking_brake, equipment, exhaust_system, energy_battery,
                         transmission, e_car, layout_scheme, seating_capacity, body_type,
                         frame, tires, axes_count, passenger_capacity, hybrid, izp, cabin, e_engine_1,
                         voltage_1, max_30_power_1, e_engine_2, voltage_2, max_30_power_2, luggage_volume, id)

            cursor.execute(query_ts, values_ts)

            connection.commit()




        except ValueError as ve:
            messagebox.showerror("Ошибка", str(ve))
            print(str(ve))
            return None
        except Exception as error:
            messagebox.showerror("Ошибка", f"Ошибка при выполнении запроса: {error}")
            print(error)
            return None
        finally:
            if connection:
                connection.close()


    def fetch_data_sbcts_archive(self, vin, brand,  model, type, engine, check_var):
        connection = self.connect_2()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            base_query = f"""SELECT vin, brand, model, type, engine, number, similarity(vin, '{vin}') AS sim_score FROM sbkts WHERE vin IS NOT NULL"""


            filters = []
            if brand:
                filters.append(f" AND sbkts.model ILIKE '%{brand}%'")
                print('1')
            if model:
                filters.append(f" AND sbkts.brand ILIKE '%{model}%'")
                print('1')
            if engine:
                filters.append(f" AND sbkts.engine ILIKE '%{engine}%'")
                print('1')
            if type:
                filters.append(f" AND sbkts.type ILIKE '%{type}%'")
                print('1')
            if check_var:
                filters.append(f" AND sbkts.number ILIKE '%ОВ49%'")
                print('1')
            if vin:
                filters.append(f" ORDER BY sim_score DESC")
                print('1')


            final_query = base_query + " ".join(filters)

            print(final_query)

            cursor.execute(final_query)
            result = cursor.fetchall()

            return  result

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка при фильтрации данных: {error}")
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()



    def fetch_data_application_archive(self, id, vin,  brand, model, owner,  date_registration=None, date_archive=None):
        connection = self.connect()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            base_query = f"""SELECT application.id, vin, brand, model, owner, customer, date_registration, date_archive, (vin, '{vin}') AS sim_score FROM application INNER
             JOIN ts_info ON application.id = ts_info.id WHERE 1=1"""


            filters = []
            if id:
                filters.append(f" AND application.id = '{id}'")
            if brand:
                filters.append(f" AND brand ILIKE '%{brand}%'")
            if model:
                filters.append(f" AND model ILIKE '%{model}%'")
            if owner:
                filters.append(f" AND owner ILIKE '%{owner}%'")
            if date_registration:
                filters.append(f" AND date_registration = '{date_registration}'")
            if date_archive:
                filters.append(f" AND date_archive = '{date_archive}'")
            if vin:
                filters.append(f" ORDER BY sim_score DESC, date_registration DESC")
            else:
                filters.append(f" ORDER BY date_registration DESC")


            final_query = base_query + " ".join(filters)


            cursor.execute(final_query)
            result = cursor.fetchall()

            return  result

        except (Exception, psycopg2.DatabaseError) as error:
            messagebox.showerror("Ошибка", f"Ошибка при фильтрации данных: {error}")
            print(error)
        finally:
            if connection:
                cursor.close()
                connection.close()









