from mlc import utils
import os
import subprocess


def check_installation(command, os_info):
    if os_info['platform'] == "windows":
        return subprocess.call(
            [command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) == 0
    elif os_info['platform'] == "linux":
        return subprocess.call(['which', command], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE) == 0  # 0 means the package is there


def preprocess(i):

    os_info = i['os_info']
    env = i['env']

    if not check_installation("numactl", os_info):
        env['MLC_INSTALL_NUMACTL'] = 'True'

    # if not check_installation("cpupower",os_info):
    env['MLC_INSTALL_CPUPOWER'] = 'True'

    if env.get('MLC_PLATFORM_DETAILS_FILE_PATH', '') == '':
        if env.get('MLC_PLATFORM_DETAILS_DIR_PATH', '') == '':
            env['MLC_PLATFORM_DETAILS_DIR_PATH'] = os.getcwd()
        if env.get('MLC_PLATFORM_DETAILS_FILE_NAME', '') == '':
            env['MLC_PLATFORM_DETAILS_FILE_NAME'] = "system-info.txt"
        env['MLC_PLATFORM_DETAILS_FILE_PATH'] = os.path.join(
            env['MLC_PLATFORM_DETAILS_DIR_PATH'], env['MLC_PLATFORM_DETAILS_FILE_NAME'])

    return {'return': 0}


def postprocess(i):

    state = i['state']

    env = i['env']

    os_info = i['os_info']

    automation = i['automation']

    return {'return': 0}
