from datetime import datetime

import allure
from assertpy import assert_that
from hamcrest import (
    starts_with,
    all_of,
    has_property,
    instance_of,
    has_properties,
    equal_to,
    has_items,
)

from clients.http.dm_api_account.models.user_envelope_details import UserEnvelopeDetails


class GetV1Account:

    @staticmethod
    def check_response_values(
            response: UserEnvelopeDetails
    ):
        with allure.step('Проверка ответа'):
            assert_that(
                response, all_of(
                    has_property('resource', has_property('login', starts_with('user'))),
                    has_property('resource', has_property('roles', has_items('Guest', 'Player'))),
                    has_property('resource', has_property('registration', instance_of(datetime))),
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

