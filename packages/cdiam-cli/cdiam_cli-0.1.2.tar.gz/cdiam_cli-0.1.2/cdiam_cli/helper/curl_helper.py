import json
from typing import Any, Dict


def _convert(data: Any, ret: Dict[str, str], key: str):
    if isinstance(data, dict):
        for k in data.keys():
            _convert(data[k], ret, f"{key}[{k}]" if key != "" else k)
    elif isinstance(data, list):
        for index, k in enumerate(data):
            _convert(data[index], ret, f"{key}[{index}]")
    else:
        if data is not None:
            ret[key] = data


def generate_curl_form_command(form_data: Dict[str, str], endpoint: str):
    command = ["curl", "-X", "POST", "-H", "Content-Type: multipart/form-data"]
    for k, v in form_data.items():

        command.append("-F")
        if v is None or v.startswith("@"):
            command.append(f'{k}={"null" if v is None  else v}')
        else:
            command.append(f'{k}="{v}"')

    command.append(endpoint)
    return command


def generate_curl_json_command(json_data: Dict[str, str], endpoint: str):
    command = ["curl", "-X", "POST", "-H", "Content-Type: application/json"]
    command.append("-d")
    command.append(json.dumps(json_data))
    command.append(endpoint)
    return command


def convert_json_to_form_data(json_object: Any):
    ret = {}
    _convert(json_object, ret, "")
    return ret
