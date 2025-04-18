from .db_models.record_model import Record, RecordManager
import threading
import queue

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

    def create_async(self, user_key: str = "", session_id: str = "", workflow_id: str = "", workflow: dict = {}, result: dict = {}):
        result_queue = queue.Queue()
        def thread_target():
            r = self.create(user_key, session_id, workflow_id, workflow, result)
            if r:
                result_queue.put((True, {}))
            else:
                result_queue.put((False, {"msg": "create task failed"}))

        thread = threading.Thread(target=thread_target)
        thread.start()
        thread.join()

        # 获取线程的返回值
        return result_queue.get()