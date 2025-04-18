import { app } from "../../scripts/app.js";
app.registerExtension({
	name: "comfyui_tracking.workflow_stats_node",
//	async beforeRegisterNodeDef(nodeType, nodeData, app) {
//        const onConnectionsChange = nodeType.prototype.onConnectionsChange;
//        nodeType.prototype.onConnectionsChange = function (side,slot,connect,link_info,output) {
//            console.log(side)
//            console.log(slot)
//            console.log(output)
//            console.log(link_info)
//            console.log("connection")
//
//            onConnectionsChange?.apply(this, arguments);
//	    }
//	}
	async setup() {
		alert("Setup complete!")
	},
})