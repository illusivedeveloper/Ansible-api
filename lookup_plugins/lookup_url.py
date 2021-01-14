#!/usr/bin/python3

import requests, json
from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase

from ansible.utils.display import Display
display = Display()

class LookupModule(LookupBase):
    def run(self, url, variables=None, **kwargs):
        ret = []
        for term in url:
            display.debug("URL lookup-: %s" % term)
            try:
                r = requests.get(term)
                if r.status_code == 200:
                    ret = r.json()
                else:                
                    raise AnsibleParserError("Error calling API.")
            except AnsibleParserError:
                raise AnsibleError("Error calling API.: %s" % term)
            return ret
