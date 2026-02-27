import datetime

import pytest
from hamcrest import (
    has_property,
    starts_with,
    assert_that,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.registration import Registration


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login,password=password,email=email)
    response = account_helper.user_login(login=login, password=password)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('user'))),
            has_property('resource', has_property('registration', instance_of(datetime.datetime))),
            has_property(
                'resource', has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )
    print(response)


@pytest.mark.parametrize(
    "login, email, password, error_message, expected_status_code", [
        ("user", "test@example.com", "12345", {
            "errors": {
                "Password": ["Short"]
            }
        }, 400),
        ("user", "testexample.com", "password123", {
            "errors": {
                "Email": ["Invalid"]
            }
        }, 400),
        ("u", "test@example.com", "password123", {
            "errors": {
                "Login": ["Short"]
            }
        }, 400),
    ]
    )

def test_post_v1_account_no_registration(account_helper, login, email, password, error_message, expected_status_code):
    registration = Registration(login=login, email=email, password=password)

    with check_status_code_http(expected_status_code=expected_status_code, expected_message=error_message):
        response = account_helper.dm_account_api.account_api.post_v1_account(registration=registration)
        print(response)












