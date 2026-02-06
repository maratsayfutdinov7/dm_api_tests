import requests


class MailhogApi:
    def __init__(
            self,
            host,
            headers=None
    ):
        # Доступ к данным через другие методы
        self.host = host
        self.headers = headers

    def get_api_v2_messages(
            self,
            limit=50
            ):
        params = {
            'limit': limit,
        }
        """
        Get user emails
        """

        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            params=params,
            verify=False
        )
        return response
