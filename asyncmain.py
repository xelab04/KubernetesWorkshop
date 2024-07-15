from flask import Flask, jsonify, send_file
from virtcluster.cluster import create_vcluster, switch_context, get_kubeconfig
import virtcluster.CreateService as CreateService
import virtcluster.GetServices as GetServices

import asyncio

app = Flask(__name__)

def create_vcluster_task(cluster_name):
    try:
        namespace = f"vcluster-{cluster_name}".lower()
        cluster_name = cluster_name.lower()
        print("Getting free nodeport")
        nodePort = GetServices.main()
        print(f"Creating service with exposed port {nodePort}")
        CreateService.main(cluster_name, namespace, nodePort)
        print("Service created")

        create_vcluster(cluster_name)
        switch_context()
        kubeconfig_path = get_kubeconfig(cluster_name, nodePort)
        print("HEEEEEEREEEE")
        return {"kubeconfig": kubeconfig_path}
    except Exception as e:
        return {"error": str(e)}

@app.route('/create_vcluster/<cluster_name>', methods=['GET'])
async def create_vcluster_endpoint(cluster_name):
    kubeconfig_path = create_vcluster_task(cluster_name)["kubeconfig"]#.strip("./")
    #task = asyncio.create_task(create_vcluster_task(cluster_name))
    #results = await asyncio.gather(task)
    #kubeconfig_path = results[0]["kubeconfig"]
    print(kubeconfig_path)
    return send_file(kubeconfig_path, as_attachment=True, download_name=f"kubeconfig-{cluster_name}.yaml")
    #return jsonify({"task_id": task}), 202  # Accepted

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

