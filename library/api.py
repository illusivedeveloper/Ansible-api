#!/usr/bin/python3

import requests
from ansible.module_utils.basic import *

def getcall(link):
    r = requests.get(link)
    if r.status_code == 200:
        module.exit_json(changed=False, response=r.json())
    else:
        module.fail_json(msg="Error calling api.")

def main():
    global module
    module_args = dict(
        action = dict(required='True', type='str'),
        url = dict(required='True', type='str'),
        data = dict(required= False, type = 'str')
    )
    module = AnsibleModule(argument_spec=module_args)

    if module.params['action'] == 'GET':
        link = "%s/posts" % (module.params['url'])
        getcall(link)


if __name__ == '__main__':
    main()