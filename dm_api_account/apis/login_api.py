import requests

from dm_api_account.models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):


    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials

    ):
        """
        Авторизация пользователя
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Выход из аккаунта текущим пользователем
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    def delete_all_v1_account_login(
            self,
            **kwargs
    ):
        """
        Выход из аккаунта текущим пользователем
        """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response
