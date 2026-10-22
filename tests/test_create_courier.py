import allure
import requests
from data import URL, ResponseMessage
from generators import get_courier_data

class TestCreateCourier:

    @allure.title("TC-CC-01: Успешное создание курьера")
    def test_create_courier_success(self, register_new_courier_and_return_login_password):
        login, password, first_name = register_new_courier_and_return_login_password

        with allure.step("Проверить, что логин не пустой"):
            assert login, "Логин не должен быть пустым"

        with allure.step("Проверить, что пароль не пустой"):
            assert password, "Пароль не должен быть пустым"

        with allure.step("Проверить, что имя не пустое"):
            assert first_name, "Имя не должно быть пустым"

    @allure.title("TC-CC-02: Запрет на создание двух курьеров с одинаковым логином")
    def test_cannot_create_duplicate_courier(self):
        first_courier = get_courier_data()

        with allure.step("Создать первого курьера"):
            r1 = requests.post(URL.CREATE_COURIER, json=first_courier)
            assert r1.status_code == 201, f"Ожидался 201, получен {r1.status_code}"
            assert r1.json().get("ok") is True

        second_courier = first_courier.copy()

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            r2 = requests.post(URL.CREATE_COURIER, json=second_courier)

        with allure.step("Убедиться, что сервер отклоняет дубликат (статус 409/400)"):
            assert r2.status_code in (409, 400), f"Ожидался 409 или 400, получен {r2.status_code}"

        with allure.step("Проверить сообщение об ошибке в ответе"):
            result = r2.json()
            assert result.get("message") == ResponseMessage.CREATED_COURIER_WITH_DUPLICATE_LOGIN

    @allure.title("TC-CC-03: Ошибка при отсутствии поля login")
    def test_missing_login_field(self):
        data = get_courier_data()
        bad_data = data.copy()
        del bad_data["login"]

        with allure.step("Отправить запрос без поля login"):
            response = requests.post(URL.CREATE_COURIER, json=bad_data)

        with allure.step("Статус должен быть 400 (ошибка валидации)"):
            assert response.status_code == 400

        with allure.step("Сообщение об ошибке должно соответствовать ожидаемому"):
            result = response.json()
            assert result.get("message") == ResponseMessage.CREATED_COURIER_WITHOUT_LOGIN_PASSWORD

    @allure.title("TC-CC-04: Ошибка при отсутствии поля password")
    def test_missing_password_field(self):
        data = get_courier_data()
        bad_data = data.copy()
        del bad_data["password"]

        with allure.step("Отправить запрос без поля password"):
            response = requests.post(URL.CREATE_COURIER, json=bad_data)

        with allure.step("Статус должен быть 400"):
            assert response.status_code == 400

        with allure.step("Сообщение об ошибке должно совпадать с константой"):
            result = response.json()
            assert result.get("message") == ResponseMessage.CREATED_COURIER_WITHOUT_LOGIN_PASSWORD

    @allure.title("TC-CC-05: firstName не является обязательным — курьер создаётся")
    def test_firstname_is_not_required(self):
        data = get_courier_data()
        no_name_data = data.copy()
        del no_name_data["firstName"]

        with allure.step("Отправить запрос без firstName"):
            response = requests.post(URL.CREATE_COURIER, json=no_name_data)

        with allure.step("Курьер должен создаться со статусом 201"):
            assert response.status_code == 201

        with allure.step("Ответ должен содержать ok=True"):
            body = response.json()
            assert body.get("ok") is True

    @allure.title("TC-CC-06: Проверка формата успешного ответа (ok=true)")
    def test_success_response_contains_ok_true(self):
        data = get_courier_data()

        with allure.step("Создать курьера"):
            response = requests.post(URL.CREATE_COURIER, json=data)

        with allure.step("Статус должен быть 201"):
            assert response.status_code == 201

        with allure.step("В теле ответа должно быть ok=True"):
            body = response.json()
            assert body.get("ok") == ResponseMessage.SUCCESS_CREATED_COURIER

    @allure.title("TC-CC-07: Отсутствие любого обязательного поля приводит к ошибке")
    def test_any_missing_required_field_returns_error(self):
        required_fields = ["login", "password"]
        base_data = get_courier_data()

        for field in required_fields:
            bad_data = base_data.copy()
            del bad_data[field]

            with allure.step(f"Отправить запрос без обязательного поля '{field}'"):
                response = requests.post(URL.CREATE_COURIER, json=bad_data)
                assert response.status_code == 400, f"Поле {field} отсутствует, но статус не 400"

            with allure.step("В ответе должно быть поле message"):
                assert "message" in response.json()