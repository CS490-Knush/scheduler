import connexion
import six

from swagger_server.models.job_params import JobParams  # noqa: E501
from swagger_server.models.job_status import JobStatus  # noqa: E501
from swagger_server.models.parameters import Parameters  # noqa: E501
from swagger_server import util
import requests
import json

flow_to_ip = {}

def submit_config(body):  # noqa: E501
    """Submit storage and computation nodes to be optimized for cplex

     # noqa: E501

    :param body: Parameters for cplex to optimize with
    :type body: dict | bytes

    :rtype: Dict[str, int]
    """
    if connexion.request.is_json:
        body = Parameters.from_dict(connexion.request.get_json())  # noqa: E501
        cplex_request = {}
        cplex_request["sourceNodes"] = body.computation_nodes
        cplex_request["destNodes"] = body.storage_nodes
        unicorn_out, flow_id = call_unicorn(body.computation_nodes, body.storage_nodes)
        cplex_request["C"] = create_C_matrix(unicorn_out)
        cplex_request["A"] = create_A_matrix(unicorn_out, flow_id)
        cplex_request["numConstraints"] = len(cplex_request["A"])
        cplex_request["jobs"] = ["j_%s" % i for i in body.computation_nodes]
        print(cplex_request)

    return 400

def call_unicorn(computation_nodes, storage_nodes):
    data = {"query-desc": []}
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    flow_id = 0
    for c in computation_nodes:
        for s in storage_nodes:
            data["query-desc"].append({"flow": {"flow-id": str(flow_id), "src-ip": c, "dst-ip": s}})
            flow_to_ip[str(flow_id)] = {"src-ip": c, "dst-ip": s}
            flow_id+=1
    print(data)
    r = requests.post('http://172.17.0.2/experimental/v1/unicorn/resource-query', data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        print("Getting unicorn failed")
        return r.status_code
    return r.json(), flow_id

def create_C_matrix(unicorn_out):
    C = []
    for bw in unicorn_out['anes']:
        C.append(int(bw['availbw']))
    print(C)
    return C

def create_A_matrix(unicorn_out, flow_id):
    # Create A matrix
    A = [[0 for i in range(flow_id)] for b in range(len(unicorn_out['anes']))]
    for idx, cstr in enumerate(unicorn_out['ane-matrix']):
        for flow in cstr:
            pos = int(flow['flow-id'])
            A[idx][pos] = 1
    print(A)


def submit_jobs(body):  # noqa: E501
    """Submit jobs to be run on configured server

     # noqa: E501

    :param body: Jobs to be run on configured server
    :type body: dict | bytes

    :rtype: JobStatus
    """
    if connexion.request.is_json:
        body = JobParams.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
