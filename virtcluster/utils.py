from kubernetes import client, config
import pprint
import random
# Configs can be set in Configuration class directly or using helper utility

def _get_list_nodes_used():
    config.load_kube_config()
    
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_service_for_all_namespaces(watch=False)
    
    service_dict = ret.to_dict()
    pprint.pprint(service_dict.keys())

    nodes_used = [svc.spec.ports[0].node_port for svc in ret.items]
    return nodes_used
        
def get_available_node_port():
    nodes_used = _get_list_nodes_used()
    while True:
        new_node_port = random.randint(30005, 32767)
        if new_node_port not in nodes_used:
            return new_node_port
    
        
if __name__ == "__main__":
    nodes_used = get_list_nodes_used()
    while True:
        new_node_port = random.randint(30005, 32767)
        if new_node_port not in nodes_used:
            print(new_node_port)