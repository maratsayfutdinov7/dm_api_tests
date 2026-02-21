from restclient.configuration import Configuration
from api_mailhog.apis.mailhog_api import MailhogApi


class MailHogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)

    def get_api_v2_messages(
            self,
            response
            ):
        pass
