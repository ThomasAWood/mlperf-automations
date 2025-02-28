from mlc import utils
import os


def preprocess(i):
    env = i['env']
    if '+PATH' not in env:
        env['+PATH'] = []
    env['+PATH'].append("$HOME/.local/bin")
    return {'return': 0}


def postprocess(i):

    env = i['env']
    env['MLC_ZEPHYR_DIR'] = os.path.join(os.getcwd(), "zephyr")

    return {'return': 0}
