import json

from requests import Response

from services.dm_api_account import DmApiAccount
from services.api_mailhog import MailHogApi

class AccountHelper:

    def __init__(
            self,
            dm_account_api: DmApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
            ):
        json_data = {
            'login': login,
            'email': email,
            'password': password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"

        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Не удалось получить письма"

        token = self.get_activation_token_by_login(login=login, response=response)
        assert token is not None, f"Токен для пользователя {login} не был получен"

        response =self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

        return  response

    def user_login(self, login:str, password:str, remember_me:bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не авторизован"
        return response

    @staticmethod
    def get_activation_token_by_login(
            login: str,
            response: Response
    ):
        for item in response.json().get('items', []):
            try:
                content_body = item.get('Content', {}).get('Body')
                if not content_body:
                    continue
                user_data = json.loads(content_body)
                if user_data.get('Login') == login:
                    url = user_data.get('ConfirmationLinkUrl', '')
                    if url:
                        token = url.split('/')[-1]
                        return token
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                continue
        return None