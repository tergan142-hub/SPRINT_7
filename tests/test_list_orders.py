import allure
import requests
from data import URL
from generators import get_base_order_payload, create_courier_and_get_data

@allure.feature("Orders")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Проверка, что в ответе на GET /orders возвращается список заказов в поле orders")
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
            params = {"page": 0, "limit": 100}
            r_list = requests.get(URL.LIST_ORDERS, params=params)
            assert r_list.status_code == 200, f"Ожидался статус 200, получен {r_list.status_code}"
            body = r_list.json()

        with allure.step("Проверить, что поле orders существует и является списком"):
            assert "orders" in body, "В ответе отсутствует поле orders"
            assert isinstance(body["orders"], list), f"Поле orders должно быть списком, а получено: {type(body['orders'])}"

        with allure.step("Убедиться, что список заказов не пуст"):
            assert len(body["orders"]) > 0, "Список заказов пуст — возможно, на стенде нет активных заказов"

        with allure.step("Каждый элемент списка должен быть словарем (структурой заказа)"):
            for idx, order in enumerate(body["orders"]):
                assert isinstance(order, dict), f"Заказ №{idx} должен быть словарем, а получен: {type(order)}"