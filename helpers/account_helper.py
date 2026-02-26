import json
import random
import string
import time

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
        registration = Registration(
             login = login,
             email = email,
             password = password
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не создан {response.json()}"

        start_time = time.time()
        token = self.get_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"

        response =self.dm_account_api.account_api.put_v1_account_token(account_token=token)
        return  response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=True,
            validate_headers=False
            ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response = self.dm_account_api.login_api.post_v1_account_login(login_credentials=login_credentials, validate_response=validate_response)
        if validate_headers:
            assert response.headers['x-dm-auth-token'], "Токен пользователя не был получен"
            assert response.status_code == 200, "Пользователь не авторизован"
        return response

    def change_email(
            self,
            login: str,
            password: str,
            email: str,
            validate_response=True

            ):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email, validate_response=validate_response)

        return response

    def auth_client(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response = False
            ):
        credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=credentials,
            validate_response = validate_response
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

    def change_password(self, login: str, email: str, old_password: str, new_password: str, token: str, validate_response=True):
        reset_password_model = ResetPassword(login=login, email=email)


        self.dm_account_api.account_api.post_v1_account_password(
        reset_password=reset_password_model, validate_response=validate_response
    )

        token_activation = self.get_activation_token_by_login(login=login, token_type='reset')

        change_password_model = ChangePassword(login=login,token=token_activation,old_password=old_password,new_password=new_password)
        return  self.dm_account_api.account_api.put_v1_account_password(change_password=change_password_model)


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
        email_new = f"{user}@{domain}"
        return email_new


