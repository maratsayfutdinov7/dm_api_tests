from contextlib import contextmanager

import requests
from requests.exceptions import HTTPError





from contextlib import contextmanager
import requests
from requests.exceptions import HTTPError


@contextmanager
def check_status_code_http(
        expected_status_code: int = requests.codes.OK,
        expected_message: [str, dict] = ''
):
    try:
        yield
        if expected_status_code not in [requests.codes.OK, requests.codes.created]:
            raise AssertionError(
                f"Ожидался статус {expected_status_code}, но запрос завершился успешно (200 OK)"
            )
        if expected_message:
            raise AssertionError(
                f"Должно быть получено сообщение об ошибке '{expected_message}', но запрос прошел успешно"
            )
    except HTTPError as e:
        actual_status = e.response.status_code
        actual_body = e.response.json()
        assert actual_status == expected_status_code, \
            f"Неверный статус код! Ожидали {expected_status_code}, получили {actual_status}. \nОтвет сервера: {actual_body}"
        if expected_message:
            if isinstance(expected_message, dict):
                for key, value in expected_message.items():
                    actual_value = actual_body.get(key)
                    assert actual_value == value, \
                        f"Ошибка в поле '{key}'. \nОЖИДАЛИ: {value} \nПОЛУЧИЛИ: {actual_value}"
            else:
                actual_title = actual_body.get('title', str(actual_body))
                assert actual_title == expected_message, \
                    f"Сообщение ошибки не совпадает! \nОЖИДАЛИ: '{expected_message}' \nПОЛУЧИЛИ: '{actual_title}'"