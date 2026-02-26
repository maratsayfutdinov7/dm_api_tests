import requests

from dm_api_account.models.account_token import AccountToken
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_envelope import UserEnvelope
from dm_api_account.models.user_envelope_details import UserEnvelopeDetails
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

