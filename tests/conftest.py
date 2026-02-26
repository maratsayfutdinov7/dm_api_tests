import datetime
import json
import random
import string
import uuid
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

@pytest.fixture(scope="function")
def auth_account_helper(mailhog_api, prepare_user):
    dm_api_configuration = DmApiConfiguration(host='http://185.185.143.231:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.register_new_user(
        login=prepare_user.login,
        password=prepare_user.password,
        email=prepare_user.email
    )
    account_helper.auth_client(
        login=prepare_user.login,
        password=prepare_user.password
    )
    return account_helper

User = namedtuple('User', ['login', 'password', 'email'])
@pytest.fixture
def prepare_user():
    unique_id = str(uuid.uuid4())[:8]
    login = f"user_{unique_id}"
    email = f"email_{unique_id}@example.com"
    password = "Password123!"
    return User(login=login, password=password, email=email)

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


@pytest.fixture(scope="function")
def get_activation_token_by_login(
        mailhog_api
        ):
    def _get_token(
            login: str,
            token_type: str = 'activation'
            ):
        response = mailhog_api.get_api_v2_messages()

        for item in response.json().get('items', []):
            try:
                content_body = item.get('Content', {}).get('Body')
                if not content_body:
                    continue

                user_data = json.loads(content_body)
                user_login = user_data.get('Login')

                if user_login == login:
                    if token_type == 'activation':
                        token_url = user_data.get('ConfirmationLinkUrl')
                        if token_url:
                            return token_url.split("/")[-1]
                    elif token_type == 'reset':
                        token_uri = user_data.get('ConfirmationLinkUri')
                        if token_uri:
                            return token_uri.split("/")[-1]
            except (json.JSONDecodeError, TypeError, KeyError):
                continue
        return None

    return _get_token