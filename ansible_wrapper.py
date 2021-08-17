import sys
from ansible import context
from ansible.module_utils._text import to_text
from ansible.cli.playbook import PlaybookCLI

import os
from ansible.module_utils._text import to_text, to_bytes
from ansible.cli import CLI
from ansible.utils.collection_loader import get_collection_name_from_path, set_collection_playbook_paths
from ansible.plugins.loader import add_all_plugin_dirs

from ansible.executor.playbook_executor import PlaybookExecutor

# Read all the arguments from the cli
args = [to_text(a, errors='surrogate_or_strict') for a in sys.argv]

# Pass them to the playbook cli object
pb_cli = PlaybookCLI(args)

# Parse the arguments
pb_cli.parse()

# The context should now contain all of our parsed arguments
#print(context.CLIARGS)

#####################################################################
### Execute a playbook
# This section is copied directly from: https://github.com/ansible/ansible/blob/stable-2.9/lib/ansible/cli/playbook.py#L71

# manages passwords
sshpass = None
becomepass = None
passwords = {}

b_playbook_dirs = []
for playbook in context.CLIARGS['args']:
    if not os.path.exists(playbook):
        raise AnsibleError("the playbook: %s could not be found" % playbook)
    if not (os.path.isfile(playbook) or stat.S_ISFIFO(os.stat(playbook).st_mode)):
        raise AnsibleError("the playbook: %s does not appear to be a file" % playbook)

    b_playbook_dir = os.path.dirname(os.path.abspath(to_bytes(playbook, errors='surrogate_or_strict')))
    # load plugins from all playbooks in case they add callbacks/inventory/etc
    add_all_plugin_dirs(b_playbook_dir)

    b_playbook_dirs.append(b_playbook_dir)

set_collection_playbook_paths(b_playbook_dirs)

playbook_collection = get_collection_name_from_path(b_playbook_dirs[0])

if playbook_collection:
    display.warning("running playbook inside collection {0}".format(playbook_collection))
    AnsibleCollectionLoader().set_default_collection(playbook_collection)

# don't deal with privilege escalation or passwords when we don't need to
if not (context.CLIARGS['listhosts'] or context.CLIARGS['listtasks'] or
        context.CLIARGS['listtags'] or context.CLIARGS['syntax']):
    (sshpass, becomepass) = pb_cli.ask_passwords()
    passwords = {'conn_pass': sshpass, 'become_pass': becomepass}

# create base objects
loader, inventory, variable_manager = pb_cli._play_prereqs()

# Fix this when we rewrite inventory by making localhost a real host (and thus show up in list_hosts())
hosts = CLI.get_host_list(inventory, context.CLIARGS['subset'])

# flush fact cache if requplaybook_pathested
if context.CLIARGS['flush_cache']:
    pb_cli._flush_cache(inventory, variable_manager)

######################################################################

# Execute the playbook file
pbex = PlaybookExecutor(
    playbooks=context.CLIARGS['args'],
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    passwords=passwords,
    )

results = pbex.run()
