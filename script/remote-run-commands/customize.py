from mlc import utils
import os


def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    cmd_string = ''

    # pre_run_cmds = env.get('MLC_SSH_PRE_RUN_CMDS', ['source $HOME/cm/bin/activate'])
    pre_run_cmds = env.get('MLC_SSH_PRE_RUN_CMDS', [])

    run_cmds = env.get('MLC_SSH_RUN_COMMANDS', [])

    run_cmds = pre_run_cmds + run_cmds

    for i, cmd in enumerate(run_cmds):
        if 'cm ' in cmd:
            # cmd=cmd.replace(":", "=")
            cmd = cmd.replace(";;", ",")
            run_cmds[i] = cmd

    cmd_string += " ; ".join(run_cmds)
    user = env.get('MLC_SSH_USER')
    password = env.get('MLC_SSH_PASSWORD', None)
    host = env.get('MLC_SSH_HOST')
    if password:
        password_string = " -p " + password
    else:
        password_string = ""
    cmd_extra = ''

    if env.get("MLC_SSH_SKIP_HOST_VERIFY"):
        cmd_extra += " -o StrictHostKeyChecking=no"
    if env.get("MLC_SSH_KEY_FILE"):
        cmd_extra += " -i " + env.get("MLC_SSH_KEY_FILE")

    ssh_command = "ssh " + user + "@" + host + \
        password_string + cmd_extra + " '" + cmd_string + "'"
    env['MLC_SSH_CMD'] = ssh_command

    return {'return': 0}


def postprocess(i):

    return {'return': 0}
