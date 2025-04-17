import json
import os
from datetime import datetime
from sys import breakpointhook
from typing import List, Optional
import nodes
from .record_handler import RecordHandler


class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False

any_type = AlwaysEqualProxy("*")

class WorkflowStats:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {}, "optional": {"anything": (any_type, {}), },
            "hidden": {"unique_id": "UNIQUE_ID", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ('output', )
    FUNCTION = "process"
    CATEGORY = "utils"

    def process(self, unique_id=None, extra_pnginfo=None, **kwargs):
        values = []
        if "anything" in kwargs:
            values = kwargs['anything']
            
        if not extra_pnginfo:
            print("Error: extra_pnginfo is empty")
        elif isinstance(extra_pnginfo, dict):
            workflow = extra_pnginfo["workflow"]
            # print(workflow)
            # 遍历节点，记录输出link
            this_node = next((x for x in workflow["nodes"] if str(x["id"]) == unique_id), None)
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
                                # copy widgets_values from node to this_node
                                this_node["widgets_values"] = node["widgets_values"]
                                print(this_node)
                                # change this_node's output
                                this_node["outputs"][0]["name"] = node["outputs"][oid]["name"]
                                this_node["outputs"][0]["type"] = node["outputs"][oid]["type"]
                                RecordHandler().create(workflow=workflow, result=this_node["widgets_values"])
                                break

        else:
            ...
        # self.increment_run_count()
        
        return (values,)

WORKFLOWSTAT_CLASS_MAPPINGS = {
    "WorkflowStats": WorkflowStats
}

WORKFLOWSTAT_DISPLAY_NAME_MAPPINGS = {
    "WorkflowStats": "Workflow Stats"
}