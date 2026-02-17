import requests

from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
            ):
        """
        Register new user
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

    def put_v1_account_token(
            self,
            token
    ):
        """
        Activate registered user
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
        response = self.put(
            path=f'/v1/account/email',
            json=json_data
        )
        return response