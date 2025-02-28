from mlc import utils
import os
import shutil
import stat


def preprocess(i):

    os_info = i['os_info']

    return {'return': 0}


def postprocess(i):

    env = i['env']
    state = i['state']

    if env['MLC_HOST_OS_TYPE'].lower() == "windows":
        binary_name = "ptd-windows-x86.exe"
    else:
        binary_name = "ptd-linux-x86"
    if env.get('MLC_MLPERF_PTD_PATH', '') == '':
        env['MLC_MLPERF_PTD_PATH'] = os.path.join(
            env['MLC_MLPERF_POWER_SOURCE'], 'PTD', 'binaries', binary_name)

    file_path = env['MLC_MLPERF_PTD_PATH']
    current_permissions = os.stat(file_path).st_mode

    # Check if the file already has execute permissions
    if not (current_permissions & stat.S_IXUSR):  # Check user execute permission
        # Add execute permissions for the user
        os.chmod(file_path, current_permissions | stat.S_IXUSR)

    env['MLC_SPEC_PTD_PATH'] = env['MLC_MLPERF_PTD_PATH']

    return {'return': 0}
