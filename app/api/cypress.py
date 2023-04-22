from . import api
from flask import jsonify, request
from ..common.common import *
from ..service.record_execution import RecordTest
from ..service.trigger_task import ConcurrentTask


@api.route("/cypress/ark/sendResult", methods=["POST"])
def cypress_result():
    data = request.get_json(force=True)
    project_info = {
        "name": "ark",
        "type": "web api",
        "tool": "cypress"
    }
    record = RecordTest()
    project_id = record.get_project_id(**project_info)
    execution_id = record.save_execution(project_id, data)
    record.update_script(project_id, data)
    return jsonify({"code": 200, "success": True, "id": execution_id})


@api.route("/cypress/ark/runTest", methods=["POST"])
def run_cypress_test():
    data = request.get_json(force=True)
    task_num = data.get("task_num")
    scope = data.get("scope")
    project_name = data.get("name")

    record = RecordTest()
    task = ConcurrentTask()

    # 获取project id
    query_project = {
        "name": project_name
    }
    project_id = record.get_project_id(**query_project)

    task_num = task.get_concurrent_num(task_num)
    task_group = record.get_script_group(scope, task_num, project_id)

    task.trigger_task(task_num, task_group)
    return jsonify({"code": 200, "success": True})
