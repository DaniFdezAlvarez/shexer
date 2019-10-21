import json


def load_string_json(raw_string):
    return json.loads(raw_string)


def load_json_file(source_file):
    with open(source_file, "r") as in_stream:
        return json.load(in_stream)