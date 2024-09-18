import json
from abc import ABC, abstractmethod

import requests

from .config_parser import config
from .log.logger import Logger
from .auth import Auth
from .utils import default_api_headers, default_source_headers


class Parser(ABC):

    def __init__(self, cnf: config.Config):
        self.cnf = cnf
        self.offset = 0  # used for scrolling vulns in response
        self.limit = None  # used for limiting number of vulns in one response
        self.api_headers = default_api_headers  # headers for receiver API
        self.source_headers = default_source_headers  # headers for source

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def get_data(self, *args):
        pass

    def validate(self):
        pass
        #todo

    @abstractmethod
    def fetch_before_send(self, vulns_to_send):
        pass

    def send_to_receiver(self, vulns_to_send):
        h = Logger()
        try:
            auth = Auth(
                self.cnf,
                self.cnf.get_receiver_url(),
                self.cnf.get_receiver_auth_type(),
                api_key=self.cnf.get_receiver_api_token()
            )
            if auth.auth_header is not None:
                h.Info("Authenticated successfully")
                self.api_headers.update(auth.get_auth_header())
            else:
                h.Info("Continuing without authentication header...")
        except Exception as e:
            h.Error(f"Failed to authenticate: {e.__str__()}")

        json_to_send = self.fetch_before_send(vulns_to_send)
        jsons_to_send = {"vulnerabilities": json_to_send}
        r = requests.post(self.cnf.get_receiver_url(),
                          json.dumps(jsons_to_send, indent=4, ensure_ascii=False), verify=False, headers=
                          self.api_headers)
        if r.status_code == 201:
            h.Info(f"Vulnerabilities sent successfully")
        else:
            h.Error(f"Vulns were not sent due to error. HTTP code: {r.status_code}. Message: {r.json()}")
        # print(json.dumps(jsons_to_send, indent=4, ensure_ascii=False))

