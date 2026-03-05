import allure


@allure.suite('Проверка метода DELETE v1/account/login/all')
class TestsDeleteV1AccountLoginAll:
    @allure.title('Выход из аккаунта со всех устройств')
    @allure.sub_suite('Позитивные проверки')
    def test_delete_v1_account_login(self, auth_account_helper):
        response = auth_account_helper.logout_client_all()
        return response