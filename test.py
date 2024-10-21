import requests
import xml.etree.ElementTree as ET
import psycopg2
from bs4 import BeautifulSoup
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import undetected_chromedriver as uc
import time
import json
from datetime import datetime

i  = 0

db_params = {
    'dbname': 'dns',
    'user': 'postgres',
    'password': '8080',
    'host': '192.168.1.76',
    'port': '5432'
}

headers = {
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

headersPrice = {
    'content-type': 'application/x-www-form-urlencoded',
    'x-requested-with': 'XMLHttpRequest'
}

cookies = {
    "qrator_jsid": "1727367197.606.TtfXVl9xsesbtfmo-tl97pl0tvp5j9i8jfl5vsat0f1k9cnig"
}


def make_request(url, headers=None, data=None, cookies=None, method='GET', retries=20):
    for attempt in range(retries):
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, cookies=cookies)
            else:
                response = requests.post(url, headers=headers, data=data, cookies=cookies)

            response.raise_for_status()  # Проверка на HTTP ошибки
            return response
        except requests.exceptions.ChunkedEncodingError as e:
            print(f"Ошибка ChunkedEncodingError: {e}. Повтор через 5 секунд.")
            time.sleep(5)
        except requests.exceptions.ConnectionError as e:
            print(f"Попытка {attempt + 1}: ошибка подключения. Повтор через 20 секунд.")
            time.sleep(20)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None
    print("Не удалось выполнить запрос после нескольких попыток.")
    return None


# Получить куки
def cookie():
    global cookies
    url = 'https://www.dns-shop.ru/'
    driver = uc.Chrome()
    driver.get(url=url)
    time.sleep(5)
    cookies = driver.get_cookies()
    driver.quit()

    # Вывести cookies
    for cookie in cookies:
        if cookie['name'] == 'qrator_jsid':
            qrator_jsid_value = cookie['value']
            cookies = {
                "qrator_jsid": qrator_jsid_value
            }
            print(cookies)


# Соединение с БД
def get_db_connection():
    return psycopg2.connect(**db_params)


# Получение товаров. Этап 1.
def load_products():
    urls = [
        'https://www.dns-shop.ru/products1.xml',
        'https://www.dns-shop.ru/products2.xml',
        'https://www.dns-shop.ru/products3.xml',
        'https://www.dns-shop.ru/products4.xml',
        'https://www.dns-shop.ru/products5.xml'
    ]
    conn = get_db_connection()
    cursor = conn.cursor()

    for url in urls:
        response = make_request(url)
        if response:
            xml_data = response.content
            root = ET.fromstring(xml_data)

            for url_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                id_part = loc.split('/')[-3]
                id_name = loc.split('/')[-2]

                insert_query = """
                INSERT INTO dns_shop (id, url, id_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """
                cursor.execute(insert_query, (id_part, loc, id_name))

            conn.commit()

    cursor.close()
    conn.close()


# Получение ИД товаров. Этап 2.
def load_name():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(f'SELECT id FROM dns_shop WHERE id2 is NULL')
    product = cursor.fetchall()

    for id in product:
        id_p = id['id']
        url = f'https://www.dns-shop.ru/product/{id_p}/'
        response = make_request(url, headers=headers, cookies=cookies)

        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_card = soup.find('div', {'class': 'container product-card'})
            if product_card:
                product_id = product_card.get('data-product-card')
                if product_id:
                    query = f"UPDATE dns_shop SET id2 = '{product_id}' WHERE id = '{id_p}'"
                    cursor.execute(query)
                    conn.commit()

            item = soup.find('meta', {'itemprop': 'position', 'content': '2'})
            if item:
                parent_li = item.find_parent('li')
                item_name = parent_li.find('span', itemprop='name').get_text()
                if item_name:
                    query = f"UPDATE dns_shop SET category = '{item_name}' WHERE id = '{id_p}'"
                    cursor.execute(query)
                    conn.commit()
        else:
            print(f"Ошибка выполнения запроса: {response.status_code if response else 'No response'}")
            cookie()

    cursor.close()
    conn.close()


# Получение имен и категорий товаров. Этап 3.
def process_ids_and_update_table(conn, cursor, ids, table_name):
    for product_id_tuple in ids:
        product_id = product_id_tuple["id2"]
        url = 'https://www.dns-shop.ru/pwa/pwa/get-product/?id=' + str(product_id)
        response = make_request(url, headers=headers, cookies=cookies)
        ЗКШТЕ
        if response and response.status_code == 200:
            response_json = response.json()
            data = response_json.get('data', {})
            name = data.get('name', 'N/A')
            code = data.get('code', 'N/A')
            category = ""

            possible_keys = [
                'Общие параметры', 'Основные параметры', 'Основные характеристики',
                'Общие характеристики', 'Общая информация', 'Классификация',
                'Общие параметры и питание', 'Данные о товаре',
                'Классификация и внешний вид', 'Характеристики'
            ]

            for key in possible_keys:
                characteristics = data.get('characteristics', {}).get(key, [])
                for item in characteristics:
                    if item.get('title') == 'Тип':
                        category = item.get('value')
                        break

            name = name.replace('"', "").replace("'", "")
            query = f"UPDATE dns_shop SET code = '{code}', name = '{name}', type =  '{category}' WHERE id2 = '{product_id}'"
            cursor.execute(query)
            conn.commit()
        else:
            print(f"Ошибка выполнения запроса: {response.status_code if response else 'No response'}")
            cookie()


def update_product_info():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(f"SELECT id2 FROM dns_shop WHERE id2 is not NULL and type is NULL")
    product = cursor.fetchall()
    process_ids_and_update_table(conn, cursor, product, 'dns_shop')

    cursor.close()
    conn.close()


# Получение цен. Этап 4.
def update_product_prices():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor2 = conn.cursor(cursor_factory=RealDictCursor)

    cursor2.execute("SELECT * FROM dns_shop WHERE code is not NULL")
    json_data = {
        "type": "product-buy",
        "containers": []
    }
    max_items = 2500
    item_count = 0

    while True:
        row = cursor2.fetchone()
        if row is None:
            break

        if item_count >= max_items:
            item_count = 0
            data = 'data=' + json.dumps(json_data)
            response = make_request('https://www.dns-shop.ru/ajax-state/product-buy/', method='POST',
                                    headers=headersPrice, data=data)
            if response and response.status_code == 200:
                response_json = response.json()
                update_prices_and_availability(cursor, response_json['data']['states'])
                json_data["containers"].clear()
                item_count = 0
                conn.commit()
            else:
                print(response.status_code if response else 'No response')

        code = row["code"]
        code2 = 'as-' + str(row["code"])
        new_value = {"id": code2, "data": {"id": row["code"]}}
        json_data["containers"].append(new_value)
        item_count += 1

    data = 'data=' + json.dumps(json_data)
    response = make_request('https://www.dns-shop.ru/ajax-state/product-buy/', method='POST', headers=headersPrice,
                            data=data)
    if response and response.status_code == 200:
        response_json = response.json()
        update_prices_and_availability(cursor, response_json['data']['states'])
    else:
        print(response.status_code if response else 'No response')

    conn.commit()
    cursor.close()
    conn.close()


def update_prices_and_availability(cursor, data):
    for product in data:
        global i
        i+=1
        print(i)
        product_id = product['data']['id']
        cursor.execute(f"SELECT price FROM dns_shop WHERE id2 = %s", [product_id])
        row = cursor.fetchone()

        old_price = 0
        if row and row['price']:
            data = row['price']
            latest_date = max(data.keys())
            old_price = data[latest_date]

        if product.get('data', {}).get('price', {}).get('onlinePay'):
            cursor.execute(f"UPDATE dns_shop SET online_pay = %s WHERE id2 = %s",
                           [product['data']['price']['onlinePay'], product_id])
        else:
            cursor.execute(f"UPDATE dns_shop SET online_pay = NULL WHERE id2 = %s", [product_id])

        if product.get('data', {}).get('notAvail'):
            cursor.execute(f"UPDATE dns_shop SET availability = False WHERE id2 = '{product_id}'")
        else:
            cursor.execute(f"UPDATE dns_shop SET availability = True WHERE id2 = '{product_id}'")

            if product.get('data', {}).get('price', {}).get('current') and product.get('data', {}).get('price', {}).get(
                    'current') != old_price:
                current_date = (datetime.now()).strftime('%Y-%m-%d')
                cursor.execute(
                    f"UPDATE dns_shop SET price = jsonb_set(price, '{{{current_date}}}', '{product['data']['price']['current']}'::jsonb, true) WHERE id2 = '{product_id}'"
                )

            if product.get('data', {}).get('price', {}).get('min') and product.get('data', {}).get('price', {}).get(
                    'min') != old_price:
                current_date = (datetime.now()).strftime('%Y-%m-%d')
                cursor.execute(
                    f"UPDATE dns_shop SET price = jsonb_set(price, '{{{current_date}}}', '{product['data']['price']['min']}'::jsonb, true) WHERE id2 = '{product_id}'"
                )

        if product.get('data', {}).get('avail') is not None:
            query = f"UPDATE dns_shop SET status = '{product.get('data', {}).get('avail')}' WHERE id2 = '{product['data']['id']}'"
            cursor.execute(query)
        else:
            query = f"UPDATE dns_shop SET status = NULL WHERE id2 = '{product['data']['id']}'"
            cursor.execute(query)


# Вызовы функций
# load_products()
# print('Товары выгружены. Этап 1 завершен')
# load_name()
# print('ID товаров получены. Этап 2 завершен')
# update_product_info()
# print('Имена и категории товаров получены. Этап 3 завершен')
update_product_prices()
print('Цены обновлены. Этап 4 завершен')
