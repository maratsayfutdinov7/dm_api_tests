from typing import Any

from json import loads

import requests
from requests import Response

import random
import string

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

import json
import structlog

from restclient.configuration import Configuration


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)

def test_put_v1_account_token():
    # Регистрация пользователя
    mailhog_configuration = Configuration(host='http://185.185.143.231:5025', disable_log=False)
    dm_api_configuration = Configuration(host='http://185.185.143.231:5051', disable_log=False)

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = 'breeze944'
    email = f'{login}@mail.ru'
    password = '12345607030'
    json_data = {
    'login': login,
    'email': email,
    'password': password
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не создан {response.json()}"

    # Получить письма из почтового ящика
    response = mailhog_api.get_api_v2_messages(response)
    assert response.status_code == 200, "Не удалось получить письма"
    # pprint.pprint(response.json())

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"


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