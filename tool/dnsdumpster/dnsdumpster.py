#
# Licensed to Odin-eye under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Odin-eye licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
import sys


class DNSDumpster():

    def __init__(self, domain):
        self.domain = domain

    def run_search(self):
        results = DNSDumpsterAPI().search(self.domain)
        return DNSDumpster.__create_output_records_from_a_info(results["dns_records"]["host"], self.domain)

    @staticmethod
    def __create_output_records_from_a_info(a_records, domain):
        output_array = []
        if len(a_records) > 0:
            for i in range(0, len(a_records)):
                # Create A record
                data = {}
                data['domain'] = domain
                data['hostname'] = a_records[i]["domain"].split()[0].replace("<br", "")
                data['ipv4'] = a_records[i]["ip"]
                output_array.append(data)
        return output_array


class DNSDumpsterAPI(object):

    def __init__(self):
        self.session = requests.Session()

    def search(self, domain):
        dnsdumpster_url = 'https://dnsdumpster.com/'

        req = self.session.get(dnsdumpster_url)
        soup = BeautifulSoup(req.content, 'html.parser')
        csrf_middleware = soup.findAll('input', attrs={'name': 'csrfmiddlewaretoken'})[0]['value']

        cookies = {'csrftoken': csrf_middleware}
        headers = {'Referer': dnsdumpster_url}
        data = {'csrfmiddlewaretoken': csrf_middleware, 'targetip': domain}
        req = self.session.post(dnsdumpster_url, cookies=cookies, data=data, headers=headers)

        if req.status_code != 200:
            print(
                "Unexpected status code from {url}: {code}".format(
                    url=dnsdumpster_url, code=req.status_code),
                file=sys.stderr,
            )
            return []

        if 'error' in req.content.decode('utf-8'):
            print("There was an error getting results", file=sys.stderr)
            return []

        soup = BeautifulSoup(req.content, 'html.parser')
        tables = soup.findAll('table')

        res = {}
        res['domain'] = domain
        res['dns_records'] = {}
        res['dns_records']['dns'] = DNSDumpsterAPI.__retrieve_results(tables[0])
        res['dns_records']['mx'] = DNSDumpsterAPI.__retrieve_results(tables[1])
        res['dns_records']['txt'] = DNSDumpsterAPI.__retrieve_txt_record(tables[2])
        res['dns_records']['host'] = DNSDumpsterAPI.__retrieve_results(tables[3])
        return res

    @staticmethod
    def __retrieve_results(table):
        res = []
        trs = table.findAll('tr')
        for tr in trs:
            tds = tr.findAll('td')
            pattern_ip = r'([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
            try:
                ip = re.findall(pattern_ip, tds[1].text)[0]
                domain = str(tds[0]).split('<br/>')[0].split('>')[1]
                header = ' '.join(tds[0].text.replace('\n', '').split(' ')[1:])
                reverse_dns = tds[1].find('span', attrs={}).text

                additional_info = tds[2].text
                country = tds[2].find('span', attrs={}).text
                autonomous_system = additional_info.split(' ')[0]
                provider = ' '.join(additional_info.split(' ')[1:])
                provider = provider.replace(country, '')
                data = {'domain': domain,
                        'ip': ip,
                        'reverse_dns': reverse_dns,
                        'as': autonomous_system,
                        'provider': provider,
                        'country': country,
                        'header': header}
                res.append(data)
            except:
                pass
        return res

    @staticmethod
    def __retrieve_txt_record(table):
        res = []
        for td in table.findAll('td'):
            res.append(td.text)
        return res
