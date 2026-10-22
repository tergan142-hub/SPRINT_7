import allure
import requests
from data import URL, LoginResponseMessage
from conftest import created_courier, assert_error_response

class TestLoginCourier:

    @allure.title("TC-LC-01: Курьер успешно авторизуется, возвращается id")
    def test_courier_login_success(self, created_courier):
        payload = {"login": created_courier["login"], "password": created_courier["password"]}

        with allure.step("Выполнить запрос авторизации"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)

        with allure.step("Статус должен быть 200"):
            assert r.status_code == 200

        with allure.step("В ответе должен быть id курьера (положительное целое число)"):
            body = r.json()
            assert "id" in body and isinstance(body["id"], int) and body["id"] > 0

    @allure.title("TC-LC-02: Ошибка при отсутствии login в запросе")
    def test_login_missing_login_field(self, created_courier):
        payload = {"password": created_courier["password"]}

        with allure.step("Отправить запрос без login"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)
            assert_error_response(r, LoginResponseMessage.MISSING_FIELD)

    @allure.title("TC-LC-03: Ошибка при отсутствии password в запросе")
    def test_login_missing_password_field(self, created_courier):
        payload = {"login": created_courier["login"]}

        with allure.step("Отправить запрос без password"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)
            assert_error_response(r, LoginResponseMessage.MISSING_FIELD)

    @allure.title("TC-LC-04: Ошибка при неверном логине")
    def test_login_wrong_login(self, created_courier):
        payload = {"login": "несуществующий_логин_12345", "password": created_courier["password"]}

        with allure.step("Отправить запрос с несуществующим логином"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)
            assert_error_response(r, LoginResponseMessage.WRONG_CREDENTIALS_404)

    @allure.title("TC-LC-05: Ошибка при неверном пароле")
    def test_login_wrong_password(self, created_courier):
        payload = {"login": created_courier["login"], "password": "неверный_пароль_123"}

        with allure.step("Отправить запрос с неверным паролем"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)
            assert_error_response(r, LoginResponseMessage.WRONG_CREDENTIALS_404)

    @allure.title("TC-LC-06: Ошибка при логине несуществующего пользователя")
    def test_login_nonexistent_user(self, created_courier):
        from generators import get_courier_data
        fake = get_courier_data()
        payload = {"login": f"new_unique_login_{fake['login']}", "password": "любой_пароль"}

        with allure.step("Отправить запрос для заведомо несуществующего пользователя"):
            r = requests.post(URL.LOGIN_COURIER, json=payload)
            assert_error_response(r, LoginResponseMessage.WRONG_CREDENTIALS_404)