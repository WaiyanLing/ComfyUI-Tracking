from .db_models.record_model import Record, RecordManager


class RecordHandler(object):
    def create(self, user_key: str = "", session_id: str = "", workflow_id: str = "", workflow: dict = {}, result: dict = {}):
        r = Record()
        r.user_key = user_key
        r.session_id = session_id
        r.workflow_id = workflow_id
        r.workflow = workflow
        r.result = result
        r = RecordManager().add_record(r)
        if r:
            return True, {}
        return False, {"msg": "create task failed"}