import allure

from clients.http.dm_api_account.models.account_token import AccountToken
from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from clients.http.dm_api_account.models.user_envelope_details import UserEnvelopeDetails
from packages.restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step('Регистрация пользователя')
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
        response.raise_for_status()
        return response

    @allure.step('Получение данных о пользователе')
    def get_v1_account(
            self,
            **kwargs
            )-> UserEnvelopeDetails:
        """
        Получение информации о пользователе
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if response.status_code == 200:
            return UserEnvelopeDetails.model_validate(response.json())
        return response

    @allure.step('Активация пользователя')
    def put_v1_account_token(
            self,
            account_token: AccountToken,
            validate_response=True
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
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменение почты')
    def put_v1_account_email(
     self,
     change_email: ChangeEmail,
     validate_response=True
    ):
        """
        Изменение почты
        """
        response = self.put(
            path=f'/v1/account/email',
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Сброс пароля')
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response = True
            ):
        """
        Сброс пароля
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Изменение пароля пользователя')
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response = True
            ):
        """
        Изменение пароля
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

