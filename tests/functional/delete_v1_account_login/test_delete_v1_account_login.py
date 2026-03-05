import allure


@allure.suite('Проверка метода DELETE v1/account/login')
class TestsDeleteV1AccountLogin:
    @allure.title('Выход из аккаунта')
    @allure.sub_suite('Позитивные проверки')
    def test_delete_v1_account_login(self, auth_account_helper):
        response = auth_account_helper.logout_client()
        return response