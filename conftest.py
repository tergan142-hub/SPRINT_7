import pytest
import requests
from data import URL
from generators import get_courier_data


@pytest.fixture
def register_new_courier():

    courier_data = get_courier_data()
    payload = {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "firstName": courier_data["firstName"],
    }
    response = requests.post(URL.CREATE_COURIER, json=payload)

    yield [courier_data["login"], courier_data["password"], courier_data["firstName"]]
    # Teardown: ничего не делаем, потому что не можем удалить без id


@pytest.fixture
def created_courier():
    courier = get_courier_data()
    r = requests.post(URL.CREATE_COURIER, json=courier)
    assert r.status_code == 201, "Не удалось создать курьера"
    yield courier


@pytest.fixture
def order_cleanup():

    tracks_to_clean = []

    def create_and_track(payload: dict):
        r = requests.post(URL.CREATE_ORDER, json=payload)
        body = r.json()
        track = body.get("track")
        if track is not None:
            tracks_to_clean.append(track)
        return track

    yield create_and_track

    for track in tracks_to_clean:
        delete_url = f"{URL.BASE_URL}/api/v1/orders/{track}"
        try:
            requests.delete(delete_url)
        except Exception:
            pass


def assert_error_response(response, expected_status_codes, expected_message_substring):

    assert response.status_code in expected_status_codes, (
        f"Ожидался один из статусов {expected_status_codes}, получен {response.status_code}"
    )
    body = response.json()
    actual_msg = body.get("message", "")
    assert expected_message_substring in actual_msg, (
        f"Сообщение не содержит ожидаемой подстроки '{expected_message_substring}'. "
        f"Получено: '{actual_msg}'"
    )