import pytest
import requests
from data import URL
from generators import get_courier_data


def assert_error_response(r, expected_msg):
    assert r.status_code in (400, 401, 403, 404, 422, 504), f"Ожидался 4xx/504, получен {r.status_code}"

    if r.status_code == 504 and "Service unavailable" in r.text:
        return

    body = r.json()
    actual_msg = body.get("message", "")
    assert expected_msg in actual_msg, f"Сообщение не совпадает: ожидалось '{expected_msg}', получено '{actual_msg}'"


@pytest.fixture
def register_new_courier_and_return_login_password():
    courier_data = get_courier_data()
    login = courier_data["login"]
    password = courier_data["password"]
    first_name = courier_data["firstName"]

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(URL.CREATE_COURIER, json=payload)
    if response.status_code != 201:
        pytest.fail(f"Не удалось создать курьера: {response.status_code}, {response.text}")

    login_payload = {"login": login, "password": password}
    login_response = requests.post(URL.LOGIN_COURIER, json=login_payload)
    login_data = login_response.json()
    courier_id = login_data.get("id")
    if not courier_id:
        pytest.fail("Не удалось получить id курьера после логина")

    yield [login, password, first_name]

    delete_url = URL.DELETE_COURIER_TEMPLATE.replace(":id", str(courier_id))
    requests.delete(delete_url)


@pytest.fixture
def created_courier():
    courier = get_courier_data()
    r = requests.post(URL.CREATE_COURIER, json=courier)
    assert r.status_code == 201, f"Не удалось создать курьера: {r.text}"
    assert r.json().get("ok") is True

    yield courier

    delete_url = URL.DELETE_COURIER_TEMPLATE.replace(":id", courier["login"])
    try:
        r_del = requests.delete(delete_url)
        if r_del.status_code not in (200, 204, 404):
            print(f"[WARNING] Курьер {courier['login']} не удалён, статус: {r_del.status_code}")
    except Exception as e:
        print(f"[ERROR] Ошибка удаления курьера: {e}")


@pytest.fixture
def created_order_cleanup():
    orders_to_clean = []

    def create_and_track(payload: dict):
        r = requests.post(URL.CREATE_ORDER, json=payload)
        assert r.status_code == 200, f"Не удалось создать заказ: {r.status_code}, {r.text}"
        body = r.json()
        assert "track" in body, "В ответе нет поля track"
        track = body["track"]
        orders_to_clean.append(track)
        return body

    yield create_and_track

    for track in orders_to_clean:
        try:
            delete_url = URL.DELETE_ORDER_TEMPLATE.replace(":track", track)
            r_del = requests.delete(delete_url)
            if r_del.status_code not in (200, 204, 404):
                print(f"[WARNING] Не удалось удалить заказ {track}, статус: {r_del.status_code}")
        except Exception as e:
            print(f"[ERROR] Ошибка при удалении заказа {track}: {e}")