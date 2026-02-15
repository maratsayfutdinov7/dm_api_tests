from typing import Any

from json import loads

import requests
from requests import Response

import random
import string

from services.api_mailhog import MailhogApi
from services.dm_api_account import DmApiAccount

import structlog

import json
from restclient.configuration import Configuration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)

def test_put_v1_account_email():
    # Регистрация пользователя
    mailhog_configuration = Configuration(host='http://185.185.143.231:5025', disable_log = False)
    dm_api_configuration = Configuration(host='http://185.185.143.231:5051', disable_log = False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailhogApi(configuration=mailhog_configuration)

    login = '5a9be3dc-f042-4a60-8124-6f2e1'
    email = f'{login}@mail.ru'
    password = '12345607030'
    json_data = {
    'login': login,
    'email': email,
    'password': password
    }

    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"Пользователь не создан {response.json()}"

    # Получить письма из почтового ящика
    response = mailhog.get_api_v2_messages(response)
    assert response.status_code == 200, "Не удалось получить письма"
    # pprint.pprint(response.json())

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"


    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не авторизован"
    # Изменение почты
    def generate_random_email():
        domains = ["example.com", "testmail.co", "sample.net"]
        user_len = random.randint(5, 10)
        user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(user_len))
        domain = random.choice(domains)
        return f"{user}@{domain}"
    email_new = generate_random_email()

    json_data = {
        'login': login,
        'password': password,
        'email': email_new,
    }

    response = account.account_api.put_v1_account_email(json_data)
    assert response.status_code == 200, "Почта не изменена"

    # Попытка входа с предыдущим email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Пользователь авторизован"

    # Получить письма из почтового ящика
    response = mailhog.get_api_v2_messages(response)
    assert response.status_code == 200, "Не удалось получить письма"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = account.login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не авторизован"

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

