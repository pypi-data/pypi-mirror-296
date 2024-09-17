import json
from ..file_manager import FileManager


def dump_json(path, json_data, cls=None):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=cls, indent=4, ensure_ascii=False)


def dump_json_safe(path, json_data, cls=None):
    with FileManager(path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, cls=cls, indent=4, ensure_ascii=False)


def dumps_json(json_data, cls=None):
    return json.dumps(json_data, cls=cls, indent=4, ensure_ascii=False)


def load_json(path: str, encoding='utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return json.load(f)


def load_json_safe(path: str, encoding='utf-8'):
    with FileManager(path, 'r', encoding=encoding) as f:
        return json.load(f)


def loads_json(json_string):
    return json.loads(json_string)
