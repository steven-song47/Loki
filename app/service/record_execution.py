from ..mapper.db_case import DBAutoExec
from datetime import datetime


class RecordTest:

    def __init__(self):
        self.operate_db = DBAutoExec()

    @staticmethod
    def _divide_tasks_by_duration(tasks, num_groups):
        # 首先，从给定的任务列表中获取每个任务的持续时间
        durations = [task["duration"] for task in tasks]
        # 然后，计算所有任务的总持续时间
        total_duration = sum(durations)
        # 计算每个分组的平均持续时间
        avg_duration = total_duration / num_groups

        # 创建一个空列表，用于存储分组后的任务列表
        groups = [[] for _ in range(num_groups)]
        # 创建一个包含num_groups个0的列表，用于存储每个分组的总持续时间
        group_duration = [0] * num_groups

        # 将任务分配到持续时间相似的组中
        for i in range(len(tasks)):
            # 找到持续时间最短的组
            min_idx = group_duration.index(min(group_duration))
            # 将当前任务添加到持续时间最短的组中
            groups[min_idx].append(tasks[i])
            # 更新该组的总持续时间
            group_duration[min_idx] += durations[i]

        # 将任务从一个组移动到另一个组，以平衡每个组的总持续时间
        for i in range(num_groups):
            while group_duration[i] < avg_duration and i < num_groups - 1:
                j = i + 1
                while j < num_groups-1 and group_duration[j] > avg_duration:
                    j += 1
                if not groups[j]:
                    break
                if j < num_groups:
                    # 将持续时间最长的任务从组j移动到组i中
                    task = groups[j].pop(0)
                    groups[i].append(task)
                    # 更新组i和组j的总持续时间
                    group_duration[i] += task["duration"]
                    group_duration[j] -= task["duration"]

        # 返回分组后的任务列表
        return groups

    def get_project_id(self, **project_info):
        project_list = self.operate_db.get_data("table_project", **project_info)
        if not project_list:
            project_id = self.operate_db.add_data("table_project", **project_info)
        else:
            project_id = project_list[0]["id"]
        return project_id

    def save_execution(self, project_id, data):
        execution_data = {
            "project_id": project_id,
            "script": data["stats"]["suites"],
            "tests": data["stats"]["tests"],
            "passes": data["stats"]["passes"],
            "failures": data["stats"]["failures"],
            "pending": data["stats"]["pending"],
            "pass_percent": int(data["stats"]["passes"] / (data["stats"]["passes"]+data["stats"]["failures"]) * 100),
            "duration": data["stats"]["duration"],
            "start_time": datetime.strptime(data["stats"]["start"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            "end_time": datetime.strptime(data["stats"]["end"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        execution_id = self.operate_db.add_data("table_execution", **execution_data)
        return execution_id

    def update_script(self, project_id, data):
        script_id_list = list()
        for script in data["results"]:
            # 查询script是否已经存在
            query_filter = {
                "project_id": project_id,
                "title": script["suites"][0]["title"]
            }
            script_list = self.operate_db.get_data("table_script", **query_filter)
            if not script_list:
                # 数据库新建 script 信息
                script_data = {
                    "project_id": project_id,
                    "title": script["suites"][0]["title"],
                    "file": script["file"],
                    "duration": 0,
                    "state": "active"
                }
                script_id = self.operate_db.add_data("table_script", **script_data)
                script_id_list.append(script_id)

                # 数据库新建 case 信息
                script_duration = 0
                for scenario in script["suites"][0]["suites"]:
                    for case in scenario["tests"]:
                        case_duration = case["duration"]
                        script_duration += case_duration
                        case_data = {
                            "script_id": script_id,
                            "name": case["title"],
                            "full_name": case["fullTitle"],
                            "scenario": scenario["title"],
                            "result": case["state"],
                            "code": case["code"],
                            "duration": case_duration,
                            "state": "inactive" if case["skipped"] else "active"
                        }
                        case_id = self.operate_db.add_data("table_case", **case_data)

                # 更新 script 的 duration 字段
                update_script = {"duration": script_duration}
                self.operate_db.update_data("table_script", script_id, **update_script)
            else:
                script_id = script_list[0]["id"]

                # 数据库更新 case 信息
                script_duration = 0
                for scenario in script["suites"][0]["suites"]:
                    for case in scenario["tests"]:
                        case_name = case["title"]
                        case_duration = case["duration"]
                        script_duration += case_duration

                        # 检查 case 是否存在
                        case_query = {
                            "script_id": script_id,
                            "name": case_name
                        }
                        case_list = self.operate_db.get_data("table_case", **case_query)
                        if case_list:
                            case_id = case_list[0]["id"]
                            case_data = {
                                "full_name": case["fullTitle"],
                                "scenario": scenario["title"],
                                "result": case["state"],
                                "code": case["code"],
                                "duration": case_duration,
                                "state": "inactive" if case["skipped"] else "active"
                            }
                            self.operate_db.update_data("table_case", case_id, **case_data)
                        else:
                            case_data = {
                                "script_id": script_id,
                                "name": case["title"],
                                "full_name": case["fullTitle"],
                                "scenario": scenario["title"],
                                "result": case["state"],
                                "code": case["code"],
                                "duration": case_duration,
                                "state": "inactive" if case["skipped"] else "active"
                            }
                            case_id = self.operate_db.add_data("table_case", **case_data)

                # 数据库更新 script 信息
                update_data = {
                    "file": script["file"],
                    "duration": script_duration,
                    "state": "active"
                }
                self.operate_db.update_data("table_script", script_id, **update_data)
                script_id_list.append(script_id)

        return script_id_list

    def get_script_group(self, scope, group_num, project_id):
        query_script = {
            "project_id": project_id,
            "state": "active"
        }
        script_list = self.operate_db.get_data("table_script", **query_script)
        script_list = [{"title": script["title"], "file": script["file"], "duration": script["duration"]} for script in
                       script_list]
        # print("origin script list:", script_list)
        groups = self._divide_tasks_by_duration(script_list, group_num)
        file_groups = list()
        for group in groups:
            group_list = list()
            for script in group:
                group_list.append(script["file"])
            file_groups.append(group_list)
        return file_groups


