import json
import os
from datetime import datetime
from sys import breakpointhook
from typing import List, Optional
import nodes
from server import PromptServer
from .record_handler import RecordHandler


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

any_type = AlwaysEqualProxy("*")

def save_record(user_key, session_id, workflow_id, workflow, result, mode):
    if mode == "sync":
        print("call create sync")
        r, rd = RecordHandler().create(user_key=user_key,
                                       session_id=session_id,
                                       workflow_id=workflow_id,
                                       workflow=workflow,
                                       result=result)
    else:
        print("call create async")
        r, rd = RecordHandler().create_async(user_key=user_key,
                                       session_id=session_id,
                                       workflow_id=workflow_id,
                                       workflow=workflow,
                                       result=result)

    print(r)

class WorkflowStats:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "user_key": ("STRING", {"default": ""}),
                "workflow_id": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "session_id": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "mode": (["sync", "async"],),
                "auto_gen_session_id": (["true", "false"],),
            },
            "optional": {
                "anything": (any_type, {}),
            },
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = (any_type, "INT")
    RETURN_NAMES = ('output', 'session_id')
    FUNCTION = "process"
    CATEGORY = "utils"

    def process(self, user_key, workflow_id, session_id, mode="async", unique_id=None, extra_pnginfo=None, auto_gen_session_id="true", **kwargs):
        values = []
        if "anything" in kwargs:
            values = kwargs['anything']
            
        if not extra_pnginfo:
            print("Error: extra_pnginfo is empty")
        else:
            workflow = extra_pnginfo["workflow"]
            nodelist = workflow.get("nodes", [])

            # print(workflow)
            # 遍历节点，记录输出link
            this_node = next((x for x in nodelist if str(x["id"]) == unique_id), None)
            inputs = this_node.get("inputs", [])
            if inputs[0]:
                link_id = inputs[0].get("link", 0)
                for node in workflow["nodes"]:
                    if "outputs" not in node:
                        continue

                    for oid, output in enumerate(node["outputs"]):
                        if "links" not in output or output["links"] is None:
                            continue

                        for lid in output.get("links", []):
                            if lid == link_id:
                                print("--------------")
                                print(node)
                                print()
                                print(this_node)
                                # change this_node's output
                                this_node["outputs"][0]["name"] = node["outputs"][oid]["name"]
                                this_node["outputs"][0]["type"] = node["outputs"][oid]["type"]
                                try:
                                    if auto_gen_session_id == "true":
                                        #微秒级
                                        session_id = int(datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])
                                    else:
                                        session_id = int(session_id)

                                    save_record(
                                        user_key=user_key,
                                        session_id=session_id,
                                        workflow_id=workflow_id,
                                        workflow=workflow,
                                        result={},
                                        mode=mode
                                    )
                                except Exception as e:
                                    print(str(e))

                                break
        
        return values, session_id

WORKFLOWSTAT_CLASS_MAPPINGS = {
    "WorkflowStats": WorkflowStats
}

WORKFLOWSTAT_DISPLAY_NAME_MAPPINGS = {
    "WorkflowStats": "Workflow Stats"
}