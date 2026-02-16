import datetime
from collections import namedtuple
from typing import Any

from json import loads

import pytest
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

from datetime import datetime

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]

)

@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'breeze{data}'
    email = f'{login}@mail.ru'
    password = '12345607030'
    User = namedtuple('User',['login', 'password', 'email'])
    user = User(login=login,password=password,email=email)
    return user


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Регистрация пользователя

    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login, password=password)













