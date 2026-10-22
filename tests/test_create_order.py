import allure
import pytest
import requests
from data import URL
from generators import get_base_order_payload

@allure.feature("Orders")
@allure.story("Проверка корректности данных заказа")
class TestOrderColorVerification:

    @allure.title("TC-OC-01: Проверка цвета BLACK после создания")
    @pytest.mark.parametrize("expected_colors", [["BLACK"]])
    def test_verify_black_color(self, expected_colors):
        payload = get_base_order_payload()
        payload["color"] = expected_colors

        with allure.step("Создать заказ с указанным списком цветов"):
            r_create = requests.post(URL.CREATE_ORDER, json=payload)
            assert r_create.status_code == 201, f"Ожидался 201, получен {r_create.status_code}"
            body_create = r_create.json()
            assert "track" in body_create and isinstance(body_create["track"], int), "Нет track или он не число"
            track = body_create["track"]

        get_url = f"{URL.BASE_URL}/api/v1/orders/track?t={track}"

        with allure.step("Получить заказ по track и проверить цвета"):
            r_get = requests.get(get_url)
            assert r_get.status_code == 200, f"Не удалось получить заказ: {r_get.status_code}"
            order_data = r_get.json()["order"]

            assert "color" in order_data, "В заказе нет поля color"
            assert set(order_data["color"]) == set(expected_colors), f"Цвет не совпадает: {order_data['color']}"

    @allure.title("TC-OC-02: Проверка обоих цветов BLACK и GREY")
    @pytest.mark.parametrize("expected_colors", [["BLACK", "GREY"]])
    def test_verify_both_colors(self, expected_colors):
        payload = get_base_order_payload()
        payload["color"] = expected_colors

        with allure.step("Создать заказ с несколькими цветами"):
            r_create = requests.post(URL.CREATE_ORDER, json=payload)
            assert r_create.status_code == 201
            track = r_create.json()["track"]

        get_url = f"{URL.BASE_URL}/api/v1/orders/track?t={track}"

        with allure.step("Получить заказ и сравнить цвета"):
            r_get = requests.get(get_url)
            assert r_get.status_code == 200
            order_data = r_get.json()["order"]

            assert "color" in order_data
            assert set(order_data["color"]) == set(expected_colors)

    @allure.title("TC-OC-03: Проверка отсутствия цвета (пустой список)")
    @pytest.mark.parametrize("expected_colors", [[]])
    def test_verify_no_color(self, expected_colors):
        payload = get_base_order_payload()
        payload["color"] = expected_colors

        with allure.step("Создать заказ без цветов"):
            r_create = requests.post(URL.CREATE_ORDER, json=payload)
            assert r_create.status_code == 201
            track = r_create.json()["track"]

        get_url = f"{URL.BASE_URL}/api/v1/orders/track?t={track}"

        with allure.step("Получить заказ и убедиться, что цвета — пустой список"):
            r_get = requests.get(get_url)
            assert r_get.status_code == 200
            order_data = r_get.json()["order"]

            if "color" in order_data:
                assert order_data["color"] == [], "Ожидается пустой список цветов"
            else:
                                pass