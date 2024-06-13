from flask import Flask, send_file, jsonify
import GetServices
import CreateCluster
import subprocess
import os
import base64
import time

app = Flask(__name__)
    
@app.route('/create_vcluster/<cluster_name>', methods=['GET'])
def create_vcluster_endpoint(cluster_name):
    try:
        nodePort = GetServices.main()
        kubeconfig_path = CreateCluster.main(cluster_name)
        return send_file(kubeconfig_path, as_attachment=True, attachment_filename=f"kubeconfig-{cluster_name}.yaml")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    #main()
    app.run(host='0.0.0.0', port=5000)
    

