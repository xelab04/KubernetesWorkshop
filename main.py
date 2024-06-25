from flask import Flask, send_file, jsonify
from virtcluster.cluster import create_vcluster, switch_context, get_kubeconfig
from virtcluster import service
from virtcluster.utils import get_available_node_port

import subprocess
import os
import base64
import time

app = Flask(__name__)


@app.route('/create_vcluster/<cluster_name>', methods=['GET'])
def create_vcluster_endpoint(cluster_name):
    try:
        namespace = f"vcluster-{cluster_name}".lower()
        cluster_name = cluster_name.lower()
        print("Getting free nodeport")
        nodePort = get_available_node_port()
        print(f"Creating service with exposed port {nodePort}")
        service.create(cluster_name, namespace, nodePort)
        print("Service created")

        create_vcluster(cluster_name)
        switch_context()
        kubeconfig_path = get_kubeconfig(cluster_name, nodePort)
        return send_file(kubeconfig_path, as_attachment=True, download_name=f"kubeconfig-{cluster_name}.yaml")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use 5001 because 5000 is used on MacOS (AirPlay)
    app.run(host='0.0.0.0', port=5001)
