class URL:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"
    CREATE_COURIER = BASE_URL + "/api/v1/courier"
    DELETE_COURIER_TEMPLATE = BASE_URL + "/api/v1/courier/:id"
    LOGIN_COURIER = BASE_URL + "/api/v1/courier/login"
    CREATE_ORDER = BASE_URL + "/api/v1/orders"
    LIST_ORDERS = BASE_URL + "/api/v1/orders"


class ResponseMessage:
    SUCCESS_CREATED_COURIER = True
    CREATED_COURIER_WITHOUT_LOGIN_PASSWORD = "Недостаточно данных для создания учетной записи"
    CREATED_COURIER_WITH_DUPLICATE_LOGIN = "Этот логин уже используется"

class LoginResponseMessage:
    MISSING_FIELD = "Недостаточно данных для входа"
    WRONG_CREDENTIALS = "Учетная запись не найдена"
    WRONG_CREDENTIALS_404 = "Учетная запись не найдена"