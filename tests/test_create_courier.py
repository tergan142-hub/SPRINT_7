import allure
import pytest
import requests
from data import URL, ResponseMessage
from generators import get_courier_data
from faker import Faker

fake = Faker()

class TestCreateCourier:

    @allure.title("Проверка успешного создания курьера")
    def test_create_courier_success(self, register_new_courier):
        login, password, first_name = register_new_courier

        with allure.step("Проверить, что логин не пустой"):
            assert login, "Логин не должен быть пустым"

        with allure.step("Проверить, что пароль не пустой"):
            assert password, "Пароль не должен быть пустым"

        with allure.step("Проверить, что имя не пустое"):
            assert first_name, "Имя не должно быть пустым"

        with allure.step("Проверить, что логин не пустой"):
            assert login, "Логин не должен быть пустым"

        with allure.step("Проверить, что пароль не пустой"):
            assert password, "Пароль не должен быть пустым"

        with allure.step("Проверить, что имя не пустое"):
            assert first_name, "Имя не должно быть пустым"


    @allure.title("Проверка запрета на создание двух курьеров с одинаковым логином")
    def test_cannot_create_duplicate_courier(self):
        first_courier = get_courier_data()

        with allure.step("Создать первого курьера"):
            r1 = requests.post(URL.CREATE_COURIER, json=first_courier)
            assert r1.status_code == 201, f"Ожидался 201, получен {r1.status_code}"
            body1 = r1.json()
            assert body1.get("ok") is True

        second_courier = first_courier.copy()

        with allure.step("Попытаться создать второго курьера с тем же логином"):
            r2 = requests.post(URL.CREATE_COURIER, json=second_courier)

        with allure.step("Убедиться, что сервер отклоняет дубликат (статус 409)"):
            assert r2.status_code == 409, f"Ожидался 409 для дубликата, получен {r2.status_code}"

        with allure.step("Строго проверить сообщение об ошибке (по документации)"):
            result = r2.json()
            expected_message = ResponseMessage.CREATED_COURIER_WITH_DUPLICATE_LOGIN
            assert result.get("message") == expected_message, (
                f"Ожидалось строгое совпадение сообщения: '{expected_message}', "
                f"получено: '{result.get('message')}'"
            )


    @pytest.mark.parametrize("field", ["login", "password"])
    @allure.title("Проверка отсутствия обязательного поля (login/password) приводит к ошибке")
    def test_missing_required_fields(self, field):
        data = get_courier_data()
        bad_data = data.copy()
        del bad_data[field]

        with allure.step(f"Отправить запрос без обязательного поля '{field}'"):
            response = requests.post(URL.CREATE_COURIER, json=bad_data)

        with allure.step(f"Статус должен быть 400 при отсутствии поля '{field}'"):
            assert response.status_code == 400, f"Для поля '{field}' ожидался статус 400, получен {response.status_code}"

        with allure.step("В ответе должно быть поле message"):
            body = response.json()
            assert "message" in body, "В ответе отсутствует поле 'message'"


    @allure.title("Проверка, что firstName не является обязательным — курьер создаётся")
    def test_firstname_is_not_required(self):
        base_data = get_courier_data()
        no_name_data = base_data.copy()

        no_name_data["login"] = fake.unique.user_name()
        
        del no_name_data["firstName"]

        with allure.step("Отправить запрос без firstName, но с уникальным логином"):
            response = requests.post(URL.CREATE_COURIER, json=no_name_data)

        with allure.step("Курьер должен создаться со статусом 201"):
            assert response.status_code == 201, f"Ожидался 201 без firstName, получен {response.status_code}"

        with allure.step("Ответ должен содержать ok=True"):
            body = response.json()
            assert body.get("ok") is True


    @allure.title("Проверка формата успешного ответа (ok=true)")
    def test_success_response_contains_ok_true(self):
        data = get_courier_data()

        with allure.step("Создать курьера"):
            response = requests.post(URL.CREATE_COURIER, json=data)

        with allure.step("Статус должен быть 201"):
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        with allure.step("В теле ответа должно быть ok=True"):
            body = response.json()
            expected = ResponseMessage.SUCCESS_CREATED_COURIER
            
            if isinstance(expected, bool):
                assert body.get("ok") == expected
            else:
                assert body.get("ok") is True, f"Ожидается ok=True, получено {body.get('ok')}"