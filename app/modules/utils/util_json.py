# coding: utf-8
import base64
import json
import os
from copy import deepcopy
import pandas as pd

from app.utils.util_log import warn


def object_to_json_string(response_dict):
    return json.dumps(response_dict, indent=2, sort_keys=False)


def json_string_to_object(json_text):
    return json.loads(json_text)


def convert_data_frame_to_json(data_frame, orient='records'):
    return data_frame.to_json(orient=orient)


def load_json_from_file(path, log=None):
    if os.path.isfile(path):
        if log:
            log(f'loading {path}...')

        with open(path, 'r') as f:
            content = f.read()
            json_root_object = json_string_to_object(content)
            return json_root_object
    else:
        warn(f'cannot load {path} file')
        return dict()


def save_to_json_file(object, path, log=None):
    if log:
        log(f'saving {path}...')

    with open(path, 'w') as f:
        json = object_to_json_string(object)
        f.write(json)


def fix_json_before_saving(object_to_json, copy_it=False):

    if copy_it:
        object_to_json = deepcopy(object_to_json)

    def walk(obj: dict):
        for k, v in obj.items():
            if isinstance(v, str) or isinstance(v, list) or isinstance(v, tuple) or isinstance(v, bool):
                pass
            elif isinstance(v, dict):
                walk(v)
            elif isinstance(v, int):
                obj[k] = int(v)
            elif isinstance(v, float):
                obj[k] = float(v)
            elif isinstance(v, pd.Series):
                obj[k] = dict(zip(v.index, v.values))
            elif isinstance(v, pd.DataFrame):
                if v.empty:
                    obj[k] = 'empty_dataframe'
                else:
                    obj[k] = convert_data_frame_to_json(v)
            else:
                raise ValueError(f'Unhandled type, add it for [{k}]=[{v}][{type(v)}]')

    walk(object_to_json)

    return object_to_json


def bytes_to_base64_string(content_as_bytes):

    if content_as_bytes:
        base64_content_as_string = base64.b64encode(content_as_bytes).decode(encoding='ascii')
    else:
        base64_content_as_string = ''

    return base64_content_as_string


def base64_string_to_bytes(base64_string):

    if base64_string:
        base64_string = base64_string.encode(encoding='ascii')
        content_as_bytes = base64.b64decode(base64_string)
    else:
        content_as_bytes = b''

    return content_as_bytes
