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

from tool.dnsdumpster.dnsdumpster import DNSDumpster
from tool.ctfr.ctfr import CTFR
import sys


def show_results(domain, results, sorted_subdomain):
    print("\n[!] ---- TARGET: {d} ---- [!] \n".format(d=domain))

    for subdomain in sorted_subdomain:
        print("[-]  {s}".format(s=subdomain))
        for r in results[subdomain]:
            print("     [+]  {s}".format(s=r))
        print()


def prepare_output(results):
    output = {}
    subdomains = []
    for r in results:
        subdomains.append(r['hostname'])
        if r['hostname'] not in output:
            output[r['hostname']] = set()
        if 'ipv4' in r:
            output[r['hostname']].add(r['ipv4'])
        else:
            output[r['hostname']].add(r['alias'])
    return output, sorted(set(subdomains))


def main(domain):
    r1 = DNSDumpster(domain=domain).run_search()
    r2 = CTFR(domain).run_search()
    results, sorted_subdomain = prepare_output(r1 + r2)
    show_results(domain, results, sorted_subdomain)


if __name__ == "__main__":
    main(sys.argv[1])
