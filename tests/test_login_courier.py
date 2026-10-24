import allure
import requests
from data import URL
from conftest import created_courier
from helpers import assert_error_response


class TestLoginCourier:

    @allure.title("Проверка, что курьер успешно авторизуется, возвращается id")
    def test_courier_login_success(self, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"],
        }

        with allure.step("Выполнить запрос авторизации"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус должен быть 200"):
            assert r.status_code == 200, f"Ожидался 200, получен {r.status_code}"

        with allure.step("В ответе должен быть id курьера (положительное целое число)"):
            body = r.json()
            assert "id" in body and isinstance(body["id"], int) and body["id"] > 0, f"Некорректный id: {body}"

    @allure.title("Проверка, что присутствует ошибка при отсутствии login в запросе")
    def test_login_missing_login_field(self, created_courier):
        payload = {"password": created_courier["password"]}

        with allure.step("Отправить запрос без login"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус 400 и сообщение о недостатке данных"):
            assert_error_response(
                r,
                expected_status_codes=(400,),
                expected_message_substring="Недостаточно данных для входа",
            )

    @allure.title("Проверка, что присутствует ошибка при отсутствии password в запросе")
    def test_login_missing_password_field(self, created_courier):
        payload = {"login": created_courier["login"]}

        with allure.step("Отправить запрос без password"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус 400 и сообщение о недостатке данных"):
            assert_error_response(
                r,
                expected_status_codes=(400,),
                expected_message_substring="Недостаточно данных для входа",
            )

    @allure.title("Проверка, что присутствует ошибка при неверном логине (статус 404)")
    def test_login_wrong_login(self, created_courier):
        payload = {"login": "несуществующий_логин_12345", "password": created_courier["password"]}

        with allure.step("Отправить запрос с несуществующим логином"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус 404 и сообщение об отсутствии учётной записи"):
            assert_error_response(
                r,
                expected_status_codes=(404,),
                expected_message_substring="Учетная запись не найдена",
            )

    @allure.title("Проверка, что присутствует ошибка при неверном пароле (статус 404)")
    def test_login_wrong_password(self, created_courier):
        payload = {"login": created_courier["login"], "password": "неверный_пароль_123"}

        with allure.step("Отправить запрос с неверным паролем"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус 404 и сообщение об отсутствии учётной записи"):
            assert_error_response(
                r,
                expected_status_codes=(404,),
                expected_message_substring="Учетная запись не найдена",
            )