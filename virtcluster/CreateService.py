from jinja2 import Template
import subprocess
import time

# Define the Jinja2 template
template_str = """
apiVersion: v1
kind: Service
metadata:
  name: {{ clusterName }}-nodeport
  namespace: {{ namespace }}
spec:
  selector:
    app: vcluster #{{ shortClusterName }}#vcluster
    release: {{ clusterName }}
  ports:
    - name: https
      port: 443
      targetPort: 443
      nodePort: {{ nodePort }}
      protocol: TCP
  type: NodePort
"""


def run_command(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()


def main(clusterName, namespace, nodePort):
  data = {
    "clusterName": clusterName,
    "namespace": namespace,
    "nodePort": nodePort
  }
  
  template = Template(template_str)
  
  rendered_str = template.render(data)
  
  with open(f"nodeport-service-{clusterName}.yaml", "w") as f:
    f.write(rendered_str)
  
  print(f"Template rendered and saved to nodeport-service-{clusterName}.yaml")
  print("Applying kubernetes manifest for nodeport service")

  try:
    print(run_command(f"kubectl create namespace {namespace}"))
    #time.sleep(2)
    run_command(f"kubectl apply -f nodeport-service-{clusterName}.yaml")
  except:
    raise KeyError("the namespace is probably already in use, aborting")


