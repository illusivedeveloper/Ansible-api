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
    if r.status_code == 201:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

def putcall(url, data):
    r = requests.put(url=url, data=data)
    if r.status_code == 200 or 204 or 201:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

def patchcall(url, data):
    r = requests.patch(url=url, data=data)
    if r.status_code == 200 or 204:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

def deletecall(url):
    r = requests.delete(url)
    if r.status_code == 200 or 202 or 204:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

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

    if module.params['action'] == 'PUT':
        url = module.params['url']
        data = json.dumps(module.params['data'])
        putcall(url, data)

    if module.params['action'] == 'PATCH':
        url = module.params['url']
        data = json.dumps(module.params['data'])
        patchcall(url, data)

    if module.params['action'] == 'DELETE':
        url = module.params['url']
        deletecall(url)

if __name__ == '__main__':
    main()