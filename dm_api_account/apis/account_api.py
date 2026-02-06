import requests


class AccountApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        # Доступ к данным через другие методы
        self.host = host
        self.headers = headers

    def post_v1_account(
            self,
            json_data
            ):
        """
        Register new user
        """

        response = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
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

        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers
        )
        return response