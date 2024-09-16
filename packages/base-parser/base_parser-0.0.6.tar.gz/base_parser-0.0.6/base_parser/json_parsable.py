import datetime
import json
import time

import requests
import utils
from vuln import VulnLoader, VulnManager
from base_parser import Parser
from auth import Auth
from log.logger import Logger


class ParserJson(Parser):

    def fetch_before_send(self, vulns_to_send):
        for vuln in vulns_to_send:
            # Adding or fixing parameters #todo beautify
            vuln.update({"parser_source": self.cnf.get_json_parser_source()})
            vuln.update({"is_archive": "0"})
            vuln.update({"cpe": ["Не определено"]})
            vuln.update({"affected": [
                {"versions": [{"status": "affected", "version": vuln.get("component_versions")[0]}],
                 "product_name": vuln.get('component_name')}]})
            for update in vuln.get("patch_links"):
                if update == "0":
                    vuln.get("patch_links")[0] = "Данные уточняются"
                if update == "1":
                    vuln.get("patch_links")[0] = "Уязвимость устранена"
            new_vuln_date = vuln.get("publish_date")[:10]
            vuln.update({"publish_date": new_vuln_date})
        return vulns_to_send

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

            current_endpoint = cnf.load_endpoint_templates()[0]
            vulns = self.get_data(cnf, current_endpoint.get("source"), current_endpoint.get("filter"))

            attribute = cnf.get_endpoint_attr_name()

            part_fields = cnf.get_endpoint_fields(current_endpoint)
            vuln = VulnLoader(part_fields)
            source_vuln_fields = list()

            for keys in part_fields:
                source_vuln_fields.append(vuln.__getattribute__(keys))

            self.extract_data(vulns, attribute, vuln, source_vuln_fields)

    def extract_data(self, vulns, attribute, loader, source_vuln_fields):
        h = Logger()
        manager_main = VulnManager()

        for vulnerability in vulns.get('data'):

            result = []

            soft_map = {item['id']: item for item in vulns['included'] if item['type'] == 'soft'}
            vendor_map = {item['id']: item for item in vulns['included'] if item['type'] == 'vendor'}
            version_map = {item['id']: item for item in vulns['included'] if item['type'] == 'version'}

            vul = self.find_key(vulnerability, attribute)

            # Adding vulns to list

            for key in source_vuln_fields:
                if type(key) is list:
                    for k in key:
                        self.create_result_vuln(
                            loader.get_key_by_value(k),
                            [self.find_key(vul, k)],
                            h,
                            manager_main,
                            vulnerability.get("id"),
                        )
                else:
                    self.create_result_vuln(
                        loader.get_key_by_value(key),
                        self.find_key(vul, key),
                        h,
                        manager_main,
                        vulnerability.get("id"),
                    )

            versions = []
            for version_data in self.find_json_relations(vulnerability):
                version_id = version_data
                version = version_map.get(version_id)
                if version:
                    versions.append({"version": version[attribute]['ver_name'], "status": "affected"})

            if versions:
                version_id = vulnerability['relationships']['versions']['data'][0]['id']
                version_info = version_map.get(version_id)
                if version_info:
                    soft_id = version_info['attributes']['sft_id']
                    soft_info = soft_map.get(str(soft_id))
                    if soft_info:
                        vendor_id = soft_info['attributes']['vnd_id']
                        vendor_info = vendor_map.get(str(vendor_id))
                        if vendor_info:
                            result.append({
                                "versions": versions,
                                "product": soft_info['attributes']['sft_name'],
                                "vendor": vendor_info['attributes']['vnd_name']
                            })

            manager_main.add_or_update_dict(vulnerability.get("id"), {"affected": result}, "affected")
        print(json.dumps(manager_main.get_dicts(), indent=4, ensure_ascii=False))

        #
        #     # Parsing CVE todo Remove hardcoded params
        #     src_to_cve = "https://bdu.fstec.ru/api/v1/IdentVals?include=vul&filter[and][identval.vul][vul_id][=]=" + vul.get(
        #         attribute).get('vul_id')
        #     time.sleep(float(cnf.get_evasion_time()))
        #     response = requests.get(src_to_cve, headers=self.source_headers, verify=False)
        #     if response.json().get('status') == 429:
        #         h.Error("Error in rate limit. Too much requests for API. Expand evasion sleep time")
        #     if 'data' in response.json():
        #         for cve in response.json().get('data'):
        #             if 'idn_id' in cve.get(attribute):
        #                 if cve.get(attribute).get('idn_id') == "1":
        #                     kes = {
        #                         f"cve": f"{"CVE-" + cve.get(attribute).get('idv_val')}"}
        #                     try:
        #                         manager_main.add_or_update_dict(
        #                             vul.get('id'), kes, key)
        #                     except Exception as e:
        #                         h.Error(f"Error during adding cve: {e}")
        #                 else:
        #                     kes = {
        #                         f"cve": f"Не определено"}
        #                     try:
        #                         manager_main.add_or_update_dict(
        #                             vul.get('id'), kes, key)
        #                     except Exception as e:
        #                         h.Error(f"Error during adding cve: {e}")
        #

    def find_rel(self, vulns, idd, source_vuln_fields, attribute, loader, manager_main, vulnerability):
        h = Logger()
        for included_object in vulns.get("included"):
            if included_object["id"] == idd:
                id_to_find_relation = self.find_json_relations(included_object)
                if id_to_find_relation:
                    for i in id_to_find_relation:
                        self.find_rel(vulns, i, source_vuln_fields, attribute, loader, manager_main,
                                      vulnerability)
                for incl_field in included_object.get(attribute):
                    for keys in source_vuln_fields:
                        if type(keys) is list:
                            for k in keys:
                                if incl_field == k:
                                    self.create_result_vuln(
                                        loader.get_key_by_value(k),
                                        [self.find_key(included_object[attribute], k)],
                                        h,
                                        manager_main,
                                        vulnerability.get("id"),
                                    )
                        else:
                            if incl_field == keys:
                                self.create_result_vuln(
                                    loader.get_key_by_value(incl_field),
                                    self.find_key(included_object[attribute], incl_field),
                                    h,
                                    manager_main,
                                    vulnerability.get("id"),
                                )

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

    def find_json_relations(self, vuln):
        h = Logger()
        res = []
        if "relationships" in vuln:
            if "versions" in vuln.get('relationships'):
                for s in vuln.get('relationships')["versions"]["data"]:
                    res.append(s.get("id"))
                return res
            if "cvss2" in vuln.get('relationships'):
                for s in vuln.get('relationships')["cvss2"]["data"]:
                    id_to_find_relation = s.get("id")
                return id_to_find_relation
            if "soft" in vuln.get('relationships'):
                if type(vuln.get("relationships")["soft"]["data"]) is list:
                    for s in vuln.get("relationships")["soft"]["data"]:
                        res.append(s.get("id"))
                else:
                    res.append(vuln.get("relationships")["soft"]["data"].get("id"))
                return res
            if "vendor" in vuln.get('relationships'):
                if type(vuln.get("relationships")["vendor"]["data"]) is list:
                    for s in vuln.get("relationships")["vendor"]["data"]:
                        res.append(s.get("id"))
                else:
                    res.append(vuln.get("relationships")["vendor"]["data"].get("id"))
                return res
            else:
                h.Error("Error during finding relationships: No such relation")
                return False
        else:
            return False
