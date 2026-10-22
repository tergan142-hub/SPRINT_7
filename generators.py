from faker import Faker
import random
import string
import requests
from data import URL

fake = Faker('ru_RU')

def get_courier_data():
    """Только генерация данных (без отправки на сервер)."""
    login = ''.join(fake.random_letters(10)).lower()

    password = fake.password(
        length=8,
        special_chars=False,
        digits=True,
        upper_case=False,
        lower_case=True
    )

    first_name = fake.first_name()

    return {
        "login": login,
        "password": password,
        "firstName": first_name
    }


def create_courier_and_get_data():
    """
    Создаёт курьера на сервере, проверяет ответ и возвращает его данные.
    Возвращает dict: {"login": "...", "password": "...", "firstName": "..."}
    """
    courier = get_courier_data()
    payload = {
        "login": courier["login"],
        "password": courier["password"],
        "firstName": courier["firstName"]
    }

    r = requests.post(URL.CREATE_COURIER, json=payload)

    # Если вдруг статус не 201 — тест сразу упадёт с понятным сообщением
    assert r.status_code == 201, f"Не удалось создать курьера: статус {r.status_code}, тело: {r.text}"
    body = r.json()
    assert body.get("ok") is True, f"Ответ не содержит ok=True: {body}"

    return courier


def delete_courier_by_login(login: str):
    """Удаляет курьера по логину. Игнорирует 404 (если курьер уже удалён)."""
    delete_url = URL.DELETE_COURIER_TEMPLATE.replace(":id", login)
    try:
        r = requests.delete(delete_url)
        if r.status_code not in (200, 204, 404):
            print(f"[WARNING] Курьер {login} не удалён, статус: {r.status_code}")
    except Exception as e:
        print(f"[ERROR] Ошибка при удалении курьера {login}: {e}")


def get_base_order_payload():
    """Базовый payload для заказа: все обязательные поля."""
    metro_station = str(fake.random_int(1, 200))
    delivery_date = fake.date(pattern="%Y-%m-%d")
    address = fake.address().replace("\n", " ").replace('"', "'")

    return {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": address,
        "metroStation": metro_station,
        "phone": fake.phone_number(),
        "rentTime": fake.random_int(1, 7),
        "deliveryDate": delivery_date,
        "comment": "Автотест заказа самоката"
    }