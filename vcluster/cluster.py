import base64
from posixpath import basename
import subprocess
import argparse

def _run_command(command):
    """Run a shell command and return its output."""
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()


def create_vcluster(cluster_name, timeout=10):
    """Create a vcluster and terminate the command after a timeout."""
    print(f"Creating vcluster '{cluster_name}'...")
    proc = subprocess.Popen(f"vcluster create {cluster_name} --connect=false", shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    try:
        proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.terminate()
        print(f"Terminated vcluster creation command after {timeout} seconds.")
    if proc.returncode == 0:
        print(f"vcluster '{cluster_name}' created successfully.")
    else:
        print(f"vcluster '{cluster_name}' creation command terminated with code {proc.returncode}.")



def switch_context():
    """Switch back to the default context."""
    print("Switching back to the default cluster context...")
    _run_command("kubectl config use-context default")
    print("Switched back to the default cluster context.")


def get_kubeconfig_path(cluster_name: str) -> str:
    """Retrieve and decode the kubeconfig for the vcluster."""
    print(f"Retrieving kubeconfig for vcluster '{cluster_name}'...")
    secret_name = f"vc-{cluster_name}"
    namespace = f"vcluster-{cluster_name}"
    encoded_kubeconfig = _run_command(
        f"kubectl get secret {secret_name} -n {namespace}" + " --template={{.data.config}}")
    print(encoded_kubeconfig)
    decoded_kubeconfig = base64.b64decode(encoded_kubeconfig).decode('utf-8')

    kubeconfig_path = f"./kubeconfig-{cluster_name}"
    with open(kubeconfig_path, "w") as f:
        f.write(decoded_kubeconfig)

    print(f"Kubeconfig for vcluster '{cluster_name}' saved to '{kubeconfig_path}'.")
    return kubeconfig_path



if __name__ == "__main__":
    parser = argparse.ArgumentParser(basename(__file__), \
        description="Create a vcluster and retrieve its kubeconfig.")
    parser.add_argument("cluster_name", help="To specify a cluster name.", type=str)
    args = parser.parse_args()

    create_vcluster(args.cluster_name)
    switch_context()
    print(get_kubeconfig_path(args.cluster_name))
