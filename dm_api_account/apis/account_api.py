import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
            ):
        """
        Регистрация пользователя
        """

        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def get_v1_account(
            self,
            **kwargs
            ):
        """
        Получение информации о пользователе
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response



    def post_v1_account_password(
            self,
            **kwargs
            ):
        """
        Запрос токена на изменение пароля
        """

        response = self.post(
            path=f'/v1/account/password',
            **kwargs
        )
        return response



    def put_v1_account_password(
            self,
            json_data
            ):
        """
        Изменение пароля
        """
        response = self.put(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        Активация пользователя
        """
        headers = {
            'accept': 'text/plain',
        }

        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
     self,
     json_data
    ):
        """
        Изменение почты
        """
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response



def post_v1_account_password(
        login,
        password
        ):
    return None