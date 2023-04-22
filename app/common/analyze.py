from common import JsonOperation


class AnalyzeData:

    def __init__(self):
        self.jfile_operate = JsonOperation()
        self.origin_data = dict()

    def get_origin_data(self, file_name, file_path):
        data = self.jfile_operate.read_json_from_file(file_name, file_path)
        return data

    def reset_origin_data(self):
        self.origin_data = ""

    def set_origin_data(self, data):
        self.origin_data = data

    def get_test_result(self):
        data = dict()
        if self.origin_data:
            data = self.origin_data["stats"]
        return data