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

def test_put_v1_account_email(account_helper,prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login,password=password, email_new=email)


