from typing import Any

from json import loads

import requests
from requests import Response

import random
import string

from helpers.account_helper import AccountHelper
from services.api_mailhog import (
    MailhogApi,
    MailHogApi,
)
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
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)


    login = '5a9be3dc-f042-4a60-8124-sadldlal'
    email = f'{login}@mail.ru'
    password = '12345607030'

    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login,password=password, email_new=email)


