from json import JSONDecodeError
from tkinter.constants import SEL_LAST

import allure
import requests

from restclient.client import RestClient


class MailhogApi(RestClient):

    @allure.step('Получение писем')
    def get_api_v2_messages(
            self,
            limit=50
            ):
        params = {
            'limit': limit,
        }
        """
        Get user emails
        """

        response = self.get(
            path=f'/api/v2/messages',
            params=params,
            verify=False
        )
        return response

