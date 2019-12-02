from common.rest_client.base_client_camunda import BaseClientCamunda

from exeptions import CamundaAPIException

client_camunda = BaseClientCamunda()


class CamundaAPI:
    workflow_steps = {
        "New": "action",
        "Moderated": "action",
        "Approved": "approved",
    }

    @classmethod
    async def init(cls, name_process_definition):
        resp = await client_camunda.get_process_definition(name_process_definition)
        process_definition_list = resp.json
        process_definition_id = process_definition_list[0]["id"] if process_definition_list else None

        if not process_definition_id:
            raise CamundaAPIException(f"Can not init process. "
                                      f"'{name_process_definition}' process definition does not exists")

        process_instance_id = await cls._start_process(process_definition_id)
        return process_instance_id

    @classmethod
    async def _start_process(cls, process_definition_id):
        resp = await client_camunda.process_definition_start(process_definition_id)
        if resp.status != 200:
            raise CamundaAPIException("Can not start process instance")

        resp_json = resp.json
        return resp_json["id"]

    @classmethod
    async def _get_current_task(cls, process_instance_id):
        resp = await client_camunda.get_current_task(process_instance_id)
        task = resp.json
        return task[0] if task else None

    @classmethod
    async def task_complete(cls, process_instance_id, name, value):
        current_task = await cls._get_current_task(process_instance_id)

        if not current_task:
            raise CamundaAPIException("Can not task complete. Task does not exists")

        if name != current_task["name"]:
            raise CamundaAPIException(f"Can not task complete. Task '{name}' not match with name current task")

        action = cls.workflow_steps[name]
        resp = await client_camunda.task_complete(current_task['id'], action, value)

        if resp.status != 204:
            raise CamundaAPIException("Can not task complete. Not valid value")
