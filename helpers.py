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