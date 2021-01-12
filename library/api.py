#!/usr/bin/python3

import requests, json
from ansible.module_utils.basic import *

def getcall(url):
    r = requests.get(url)
    if r.status_code == 200:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

def postcall(url, data):
    r = requests.post(url=url, data=data)
    module.exit_json(changed=False, response=r.json())


def main():
    global module
    module_args = dict(
        action = dict(required=True, type='str'),
        url = dict(required=True, type='str'),
        data = dict(required=False, type = 'str'),
        headers = dict(required=False, type='str')
    )
    module = AnsibleModule(argument_spec=module_args)

    if module.params['action'] == 'GET':
        url = module.params['url']
        getcall(url)

    if module.params['action'] == 'POST':
        url = module.params['url']
        data = json.dumps(module.params['data'])
        postcall(url, data)

if __name__ == '__main__':
    main()