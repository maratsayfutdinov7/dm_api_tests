from clients.http.api_mailhog.apis.mailhog_api import MailhogApi
from packages.restclient.configuration import Configuration



class MailHogApi:
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.mailhog_api = MailhogApi(configuration=self.configuration)

    def get_api_v2_messages(
            self,
            response
            ):
        pass
