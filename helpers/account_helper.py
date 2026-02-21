import json
import random
import string
import time

from services.api_mailhog import MailHogApi
from services.dm_api_account import DmApiAccount


def retrier(
        function
        ):
    def wrapper(
            *args,
            **kwargs
            ):
        token = None
        count = 0
        # Вытягиваем token_type для логов (по умолчанию 'activation')
        t_type = kwargs.get('token_type', 'activation')

        while token is None:
            count += 1
            print(f'Попытка {count}: поиск токена типа "{t_type}"')

            token = function(*args, **kwargs)

            if token:
                return token

            if count >= 5:
                raise AssertionError(f"Не удалось получить токен '{t_type}' после {count} попыток")

            time.sleep(1)
        return None

    return wrapper




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

        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"

        response =self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

        return  response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
            ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не авторизован"
        return response

    def change_email(
            self,
            login: str,
            password: str,
            email_new: str
            ):
        json_data = {
            'login': login,
            'password': password,
            'email': email_new,
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "Почта не изменена"

        return response

    def auth_client(
            self,
            login: str,
            password: str
            ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                'login': login,
                'password': password
            }
            )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def logout_client(
            self
            ):

        response = self.dm_account_api.login_api.delete_v1_account_login()
        return response

    def logout_client_all(
            self
            ):

        response = self.dm_account_api.login_api.delete_all_v1_account_login()
        return response

    def get_messages(
            self
            ):

        response = self.dm_account_api.login_api.delete_all_v1_account_login()
        return response

    def change_password(self, login: str, email: str, old_password: str, new_password: str):
        self.dm_account_api.account_api.post_v1_account_password(
            json={
                "login": login,
                "email": email
            }
        )

        token_activation = self.get_activation_token_by_login(login=login, token_type='reset')
        self.dm_account_api.account_api.put_v1_account_password(
            json={
                "login": login,
                "oldPassword": old_password,
                "newPassword": new_password,
                "token": token_activation
            }
        )

    @retrier
# Получение токена активационного и для сброса пароля
    def get_activation_token_by_login(
            self,
            login: str,
            token_type: str = 'activation'

    ):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json().get('items', []):
            try:
                content_body = item.get('Content', {}).get('Body')
                if not content_body:
                    continue
                user_data = json.loads(content_body)
                user_login = user_data.get('Login')
                print(user_login)
                activation_token = user_data.get('ConfirmationLinkUrl')
                reset_token = user_data.get('ConfirmationLinkUri')
                print(activation_token)
                print(reset_token)
                if user_login == login and activation_token and token_type == 'activation':
                    return activation_token.split("/")[-1]
                elif user_login == login and reset_token and token_type == 'reset':
                    return reset_token.split("/")[-1]
            except (json.JSONDecodeError, TypeError, KeyError):
                continue
        return None

    @staticmethod
    def generate_random_email():
        domains = ["example.com", "testmail.co", "sample.net"]
        user_len = random.randint(5, 10)
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(user_len))
        domain = random.choice(domains)
        return f"{user}@{domain}"
    email_new = generate_random_email()

