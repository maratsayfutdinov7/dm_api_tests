import allure

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)
@allure.suite('Проверка метода PUT v1/account/email')
class TestsPutV1AccountEmail:
    @allure.title('Изменение почты')
    @allure.sub_suite('Позитивные проверки')
    def test_put_v1_account_email(self, account_helper, prepare_user, generate_random_email):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        email_new = generate_random_email

        account_helper.register_new_user(login=login,password=password,email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_email(login=login,password=password, email=email_new)


