import copy
from datetime import datetime, timedelta
import json, yaml, ast, time, os, re


# class YamlOperation:
#
#     def __init__(self):
#         self.root_path = os.getcwd()
#
#     def write_yaml(self, name, data, path=None):
#         if path:
#             file_path = path + name
#         else:
#             file_path = self.default_path + name
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(yaml.dump(data, allow_unicode=True, sort_keys=False))
#
#     def read_yaml(self, name, path=None):
#         if path:
#             file_path = path + name
#         else:
#             file_path = self.default_path + name
#         with open(file_path, encoding="utf-8") as f:
#             data = yaml.load(f, Loader=yaml.FullLoader)
#             print(data)
#         return data


class JsonOperation:

    def __init__(self):
        self.root_path = "/".join(os.path.split(os.path.realpath(__file__))[0].split("/")[:-2]) + "/"

    def write_json_to_file(self, file_name, json_data, file_path=None, encoding="utf-8"):
        if not file_path:
            file_path = self.root_path
        with open(file_path + file_name, "w", encoding=encoding) as f:
            f.write(json.dumps(json_data, ensure_ascii=False))

    def read_json_from_file(self, file_name, file_path=None, encoding="utf-8"):
        if file_path:
            file_path = self.root_path + file_path
        else:
            file_path = self.root_path
        with open(file_path + file_name, "r", encoding=encoding) as f:
            if ".json" in file_name:
                data = json.loads(f.read())
            else:
                data = f.read()
        return data


if __name__ == "__main__":
    j = JsonOperation()
    data = j.read_json_from_file("cypress_2023-03-23.json", "test/")
    print(data)