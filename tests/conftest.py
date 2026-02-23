import datetime
import random
import string
from collections import namedtuple

import pytest

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

@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://185.185.143.231:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client

@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    return account

@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope="session")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login='breeze17_02_2026_11_01_43',
        password='12345607030'
    )
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

@pytest.fixture
def generate_random_email():
    domains = ["example.com", "testmail.co", "sample.net"]
    user_len = random.randint(5, 10)
    user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(user_len))
    domain = random.choice(domains)
    email_new = f"{user}@{domain}"
    return  email_new

@pytest.fixture
def generate_random_password():
    length = random.randint(8, 12)
    characters = string.ascii_letters + string.digits
    new_password = ''.join(random.choice(characters) for _ in range(length))
    return new_password