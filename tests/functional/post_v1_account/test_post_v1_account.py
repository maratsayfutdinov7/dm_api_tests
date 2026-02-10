from typing import Any

from json import loads

import requests
from requests import Response

import random
import string

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)

def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(host='http://185.185.143.231:5051')
    login_api = LoginApi(host='http://185.185.143.231:5051')
    mailhog_api = MailhogApi(host='http://185.185.143.231:5025')
    login = 'breeze153'
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


    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
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

    response = account_api.put_v1_account_email(json_data)
    assert response.status_code == 200, "Почта не изменена"

    # Попытка входа с предыдущим email
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, "Пользователь авторизован"

    # Получить письма из почтового ящика
    response = mailhog_api.get_api_v2_messages(response)
    assert response.status_code == 200, "Не удалось получить письма"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизация пользователя
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True
    }
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, "Пользователь не авторизован"



def get_activation_token_by_login(
        login: str,
        response: Response
        ) -> Any:
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    return token







