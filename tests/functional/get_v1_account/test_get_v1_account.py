import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http


@allure.suite('Проверка метода GET v1/account')
class TestsGetV1Account:
    @allure.title('Получение информации о пользователе')
    @allure.sub_suite('Позитивные проверки')
    def test_get_v1_account(self, auth_account_helper):
        with allure.step('Аутентификация и авторизация пользователя для получения информации о пользователе'):
            with check_status_code_http():
                response = auth_account_helper.dm_account_api.account_api.get_v1_account()
                GetV1Account.check_response_values(response)
                print(response)
    @allure.title('Попытка авторизовать несуществующего в системе пользователя')
    @allure.sub_suite('Негативные проверки')
    def test_get_v1_account_no_auth(self, account_helper):
        with allure.step('Попытка авторизовать несуществующего в системе пользователя'):
            with check_status_code_http(401, 'User must be authenticated'):
                account_helper.dm_account_api.account_api.get_v1_account()