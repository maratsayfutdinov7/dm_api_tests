

import allure
import pytest


from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from clients.http.dm_api_account.models.registration import Registration





@allure.suite('Проверка метода POST v1/account')
class TestsPostV1Account:
    @allure.title('Регистрация и активация пользователя')
    @allure.sub_suite('Позитивные проверки')
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password)
        PostV1Account.check_response_values(response)


    @pytest.mark.parametrize(
        "login, email, password, error_message, expected_status_code", [
            ("user", "test@example.com", "12345", {
                "errors": {
                    "Password": ["Short"]
                }
            }, 400),
            ("user", "testexample.com", "password123", {
                "errors": {
                    "Email": ["Invalid"]
                }
            }, 400),
            ("u", "test@example.com", "password123", {
                "errors": {
                    "Login": ["Short"]
                }
            }, 400),

        ],
            ids = [
            "Короткий пароль",
            "Некорректный email",
            "Короткий логин"
        ]
    )
    @allure.sub_suite('Негативные проверки')
    def test_post_v1_account_no_registration(
            self,
            account_helper,
            login,
            email,
            password,
            error_message,
            expected_status_code,
            request
            ):
        registration = Registration(login=login, email=email, password=password)

        with allure.step("Регистрация пользователя (негативный кейс)"):
            with check_status_code_http(expected_status_code=expected_status_code, expected_message=error_message):
                account_helper.dm_account_api.account_api.post_v1_account(registration=registration)
        allure.dynamic.title(f"Пользователь не зарегистрирован: {request.node.callspec.id}")













