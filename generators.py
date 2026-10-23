import string
import random
import requests
from faker import Faker
from data import URL

fake = Faker("ru_RU")


def get_courier_data():
    login = fake.unique.user_name()
    password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    first_name = fake.first_name()
    return {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

def create_courier_and_get_data():
    courier = get_courier_data()
    r = requests.post(URL.CREATE_COURIER, json=courier)
    # Можно добавить assert, если хочешь, чтобы при ошибке создания сразу падал генератор
    if r.status_code != 201:
        raise RuntimeError(f"Не удалось создать курьера, статус: {r.status_code}, тело: {r.text}")
    return courier

def get_base_order_payload():
    return {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": str(random.randint(1, 20)),
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2024-12-10",
        "comment": "Тестовый заказ",
        "color": ["BLACK"],
    }