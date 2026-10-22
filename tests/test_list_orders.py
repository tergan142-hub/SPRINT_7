import allure
import pytest
import requests
from data import URL
from generators import get_base_order_payload, create_courier_and_get_data, delete_courier_by_login

@allure.feature("Orders")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("TC-OL-01: В ответе на GET /orders возвращается список заказов в поле orders")
    def test_orders_list_returns_array(self):
        with allure.step("Создать курьера для работы с заказами"):
            courier = create_courier_and_get_data()

        tracks = []
        for i in range(2):
            with allure.step(f"Создать заказ №{i + 1}"):
                payload = get_base_order_payload()
                r_create = requests.post(URL.CREATE_ORDER, json=payload)
                assert r_create.status_code == 201, f"Не удалось создать заказ: {r_create.status_code}"
                track = r_create.json()["track"]
                tracks.append(track)

        with allure.step("Получить список заказов"):
            r_list = requests.get(URL.LIST_ORDERS)
            assert r_list.status_code == 200, f"Ожидался 200 для списка заказов, получен {r_list.status_code}"
            body = r_list.json()

        with allure.step("Проверить структуру ответа: наличие поля orders и его тип"):
            assert "orders" in body, "В ответе нет поля orders"
            assert isinstance(body["orders"], list), f"Поле orders должно быть списком, а получено: {type(body['orders'])}"

        with allure.step("Убедиться, что в списке есть созданные заказы"):
            assert len(body["orders"]) >= 2, f"В списке orders меньше элементов, чем создали: {len(body['orders'])}"

        with allure.step("Каждый элемент списка должен быть словарем (заказом)"):
            for order in body["orders"]:
                assert isinstance(order, dict), "Каждый заказ в orders должен быть словарем"

        with allure.step("Удалить курьера (очистка стенда)"):
            delete_courier_by_login(courier["login"])