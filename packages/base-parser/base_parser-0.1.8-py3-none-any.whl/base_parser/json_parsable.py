import json
from abc import abstractmethod
import requests
from .vuln import (
    VulnLoader,
    VulnManager
)
from .base_parser import Parser
from .auth import Auth
from .log.logger import Logger


class ParserJson(Parser):

    @abstractmethod
    def fetch_before_send(self, vulns_to_send):
        pass

    @abstractmethod
    def extract_data(self, vulns, attribute, vuln, source_vuln_fields, manager_main):
        h = Logger()
        h.Error("Got vulnerabilities, but extraction method not implemented")

    def parse(self):
        cnf = self.cnf
        h = Logger()

        if cnf.get_endpoint_limit() is Exception:
            h.Error("Failed to get limit. Setting to None...")
        else:
            self.limit = cnf.get_endpoint_limit()

        if cnf.get_endpoint_filters() is Exception:
            h.Error("Failed to get filter. Setting to None...")
        else:
            self.filter = cnf.get_endpoint_filters()

        try:
            auth = Auth(
                cnf,
                self.cnf.get_source_source() + self.cnf.get_features_auth_url(),
                self.cnf.get_features_auth_type(),
                auth_endpoint=self.cnf.get_features_auth_url()
            )
            if auth.auth_header is not None:
                h.Info("Authenticated successfully")
                self.source_headers.update(auth.get_auth_header())
            else:
                h.Info("Continuing without authentication header...")
        except Exception as e:
            h.Error("Failed to authenticate: " + e.__str__())

        vulns = 0

        while vulns is not None:

            manager_main = VulnManager()

            for current_endpoint in cnf.load_endpoint_templates():
                vulns = self.get_data(cnf, current_endpoint.get("source"), current_endpoint.get("filter"))

                attribute = cnf.get_endpoint_attr_name()

                part_fields = cnf.get_endpoint_fields(current_endpoint)
                vuln = VulnLoader(part_fields)
                source_vuln_fields = list()

                for keys in part_fields:
                    source_vuln_fields.append(vuln.__getattribute__(keys))

                self.extract_data(vulns, attribute, vuln, source_vuln_fields, manager_main)

            self.send_to_receiver(manager_main.get_dicts())

    def create_result_vuln(self, init_key, data, h, manager, ids):
        to_add = {
            f"{init_key}": data}
        try:
            manager.add_or_update_dict(
                ids,
                to_add,
                init_key
            )
        except Exception as e:
            h.Error(f"Error during adding vul list: {e}")

    def get_data(self, cnf, current_endpoint, filters):
        source_url = cnf.get_source_source() + current_endpoint + filters  # todo
        r = requests.get(source_url, headers=self.source_headers, verify=False)
        return r.json()

    def find_key(self, data, target_key):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    return value
                elif isinstance(value, (dict, list)):
                    result = self.find_key(value, target_key)
                    if result is not None:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = self.find_key(item, target_key)
                if result is not None:
                    return result
        return None
