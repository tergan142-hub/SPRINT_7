import allure
import pytest
import requests
from data import URL
from generators import get_base_order_payload

@allure.feature("Orders")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверка  успешного создания заказа, проверка track и статуса 201")
    def test_create_order_success(self, order_cleanup):
        payload = get_base_order_payload()

        with allure.step("Отправить POST /api/v1/orders с валидными данными"):
            r_create = requests.post(URL.CREATE_ORDER, json=payload)

        with allure.step("Статус ответа должен быть 201 Created"):
            assert r_create.status_code == 201, f"Ожидался 201, получен {r_create.status_code}"

        with allure.step("В ответе должно быть поле track, и оно должно быть целым числом"):
            body_create = r_create.json()
            assert "track" in body_create, "В ответе нет поля track"
            assert isinstance(body_create["track"], int), "track не является целым числом"


    @allure.title("Проверка создания заказа со списком цветов (цвет не возвращается в ответе)")
    @pytest.mark.parametrize("colors", [["BLACK"], ["BLACK", "GREY"]])
    def test_create_order_with_colors(self, colors, order_cleanup):
        payload = get_base_order_payload()
        payload["color"] = colors

        with allure.step(f"Создать заказ со списком цветов: {colors}"):
            r_create = requests.post(URL.CREATE_ORDER, json=payload)
            assert r_create.status_code == 201, f"Ожидался 201, получен {r_create.status_code}"
            body = r_create.json()

        with allure.step("Проверить, что в ответе есть track и он число"):
            assert "track" in body and isinstance(body["track"], int), "Нет track в ответе"


        assert payload.get("color") == colors, "Цвета в payload не совпадают с переданными"

    @allure.title("Заказ создаётся даже при отсутствии firstName (валидация на стенде отсутствует)")
    def test_missing_first_name(self):
        payload = get_base_order_payload()
        del payload["firstName"]

        with allure.step("Отправить запрос без firstName"):
            response = requests.post(URL.CREATE_ORDER, json=payload)

        with allure.step("Стенд создаёт заказ и возвращает 201"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            body = response.json()
            assert "track" in body and isinstance(body["track"], int), "Нет track в ответе"

    @allure.title("Заказ создаётся даже при отсутствии lastName (валидация на стенде отсутствует)")
    def test_missing_last_name(self):
        payload = get_base_order_payload()
        del payload["lastName"]

        with allure.step("Отправить запрос без lastName"):
            response = requests.post(URL.CREATE_ORDER, json=payload)

        with allure.step("Стенд создаёт заказ и возвращает 201"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            body = response.json()
            assert "track" in body and isinstance(body["track"], int), "Нет track в ответе"