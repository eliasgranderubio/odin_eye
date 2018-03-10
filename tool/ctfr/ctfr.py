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

import requests
import json
import dns.resolver


class CTFR():

    def __init__(self, domain):
        self.domain = domain

    def run_search(self):
        r = requests.get("https://crt.sh/?q=%." + self.domain + "&output=json")
        output = []
        if r.status_code == 200:
            json_data = json.loads('[{}]'.format(r.text.replace('}{', '},{')))
            subdomains = []
            for (key, value) in enumerate(json_data):
                if value['name_value'].lower() not in subdomains and "*" not in value['name_value']:
                    subdomains.append(value['name_value'].lower())
            subdomains = sorted(set(subdomains))
            for subdomain in subdomains:
                r = CTFR.run_dns_query(self.domain, subdomain)
                if len(r) > 0:
                    output += r
        return output

    @staticmethod
    def run_dns_query(domain, subdomain):
        # Init
        dns_resolver = dns.resolver.Resolver()
        dns_resolver.timeout = 2
        dns_resolver.lifetime = 2
        output = []

        # Prepare CNAME query
        try:
            answers = dns_resolver.query(subdomain, 'CNAME', raise_on_no_answer=False)
            # Process the answers
            if type(answers) is not None and type(answers) is not TypeError:
                for answer in answers:
                    data = {}
                    data['domain'] = domain
                    data['hostname'] = subdomain
                    data['alias'] = str(answer)[:-1]
                    output.append(data)
        except:
            # No matter
            pass

        if len(output) == 0:
            # Prepare A query
            try:
                answers = dns_resolver.query(subdomain, 'A', raise_on_no_answer=False)
                # Process the answers
                if type(answers) is not None and type(answers) is not TypeError:
                    for answer in answers:
                        data = {}
                        data['domain'] = domain
                        data['hostname'] = subdomain
                        data['ipv4'] = str(answer)
                        output.append(data)
            except:
                # No matter
                pass

        # Return
        return output
