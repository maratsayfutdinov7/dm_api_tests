import requests

from dm_api_account.models.account_token import AccountToken
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.registration import Registration
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration
            ):
        """
        Регистрация пользователя
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
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

    def put_v1_account_token(
            self,
            account_token: AccountToken
    ):
        """
        Активация пользователя
        """
        headers = {
            'accept': 'text/plain',
        }

        response = self.put(
            path=f'/v1/account/{account_token}',
            headers=headers
        )
        return response

    def put_v1_account_email(
     self,
     change_email: ChangeEmail
    ):
        """
        Изменение почты
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
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
            **kwargs
            ):
        """
        Изменение пароля
        """
        response = self.put(
            path=f'/v1/account/password',
            **kwargs
        )
        return response