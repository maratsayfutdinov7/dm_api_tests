from typing import Any

from json import loads

import requests

import json
from requests import Response

import random
import string

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

from services.api_mailhog import (
    MailHogApi,
)
from services.dm_api_account import DmApiAccount


import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)

def test_post_v1_account():
    # Регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025', disable_log = False)
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log = False)

    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'bfb1f7e9-0d1e-43cc-8ab3-osdas0di0xzc'
    email = f'{login}@mail.ru'
    password = '12345607030'
    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login, password=password)













