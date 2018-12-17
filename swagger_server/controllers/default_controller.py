import connexion
import six

from swagger_server.models.job_params import JobParams  # noqa: E501
from swagger_server.models.job_status import JobStatus  # noqa: E501
from swagger_server.models.parameters import Parameters  # noqa: E501
from swagger_server import util
import requests
import json
import time
import datetime

flow_to_ip = {}
vip_to_ip = {"10.0.0.251": "172.17.0.3", "10.0.0.252": "172.17.0.4", "10.0.0.253": "172.17.0.5", "10.0.0.254": "172.17.0.6"}
computation_nodes = []

def submit_config(body):  # noqa: E501
    """Submit storage and computation nodes to be optimized for cplex

     # noqa: E501

    :param body: Parameters for cplex to optimize with
    :type body: dict | bytes

    :rtype: Dict[str, int]
    """
    start_time = time.time()
    global computation_nodes
    if connexion.request.is_json:
        body = Parameters.from_dict(connexion.request.get_json())  # noqa: E501
        cplex_request = {}
        computation_nodes = body.computation_nodes

        cplex_request["sourceNodes"] = body.computation_nodes
        cplex_request["destNodes"] = body.storage_nodes
        unicorn_out, flow_id = call_unicorn(body.computation_nodes, body.storage_nodes)
        cplex_request["C"] = create_C_matrix(unicorn_out)
        cplex_request["A"] = create_A_matrix(unicorn_out, flow_id)
        cplex_request["numConstraints"] = len(cplex_request["A"])
        cplex_request["jobs"] = ["j_%s" % i for i in body.computation_nodes]

        print(cplex_request)
        bimatrix = run_cplex(cplex_request)
        # Send to computation nodes using tc
        tc_computation_nodes(bimatrix)
        total_time = time.time() - start_time
        log(len(body.computation_nodes), len(body.storage_nodes), total_time)
        return 200
    return 400


def log(num_comp_nodes, num_storage_nodes, total_time):
    file_name = 'scheduler_{date:%Y-%m-%d_%H-%M-%S}.txt'.format(date=datetime.datetime.now())
    with open(file_name, 'a') as f:
         f.write("Current Time,Num Computation Nodes,Num Storage Nodes,Total Time\n")
         f.write("%s,%s,%s,%s\n" % (str(time.time()), str(num_comp_nodes), str(num_storage_nodes), str(total_time)))


def call_unicorn(computation_nodes, storage_nodes):
    data = {"query-desc": []}
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    flow_id = 0
    for c in computation_nodes:
        for s in storage_nodes:
            data["query-desc"].append({"flow": {"flow-id": str(flow_id), "src-ip": c, "dst-ip": s}})
            flow_to_ip[flow_id] = {"src-ip": c, "dst-ip": s}
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
    return A

def run_cplex(cplex_request):
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://35.196.13.25:8080/cpsc490/cplex_server/1.0.0/optimize', data=json.dumps(cplex_request), headers=headers)
    if r.status_code == 200:
        print("Successful optimization")
    job_code = int(r.json())
    print(job_code)
    bimatrix = []
    while bimatrix == []:
        r = requests.get('http://35.196.13.25:8080/cpsc490/cplex_server/1.0.0/status/%d' % job_code)
        if r.status_code != 200:
            print("error getting job status...")
            return
        if r.json()['status'] != 'done':
            time.sleep(2)
            print("Job is not done")
            continue
        bimatrix_req = requests.get('http://35.196.13.25:8080/cpsc490/cplex_server/1.0.0/bijobmatrix/%d' % job_code)
        if bimatrix_req.status_code == 200:
            bimatrix = bimatrix_req.json()
    print("Optimization complete...")
    print(bimatrix)
    return bimatrix

def tc_computation_nodes(bimatrix):
    # fill in
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    for idx, flow in enumerate(bimatrix):
        if flow != 0: # we are using this flow
            print("Using flow %d" % idx)
            ips = flow_to_ip[idx]
            # lookup from vip -> other one
            src_ip = vip_to_ip[ips["src-ip"]]
            dst_ip = vip_to_ip[ips["dst-ip"]]

            data = {"storage_ip": ips["dst-ip"], "bandwidth": flow}
            print(json.dumps(data))
            r = requests.post('http://%s/tc' % src_ip, data=json.dumps(data), headers=headers)
            if r.status_code == 200:
                print("TC successful - computation node")
            r = requests.post('http://%s/tc' % dst_ip, data=json.dumps(data), headers=headers)
            if r.status_code == 200:
                print("TC successful - storage node")

def submit_jobs(body):  # noqa: E501
    """Submit jobs to be run on configured server

     # noqa: E501

    :param body: Jobs to be run on configured server
    :type body: dict | bytes

    :rtype: JobStatus
    """
    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}
    computation_nodes_copy = list(computation_nodes)
    print(computation_nodes)
    print("Copy:" , computation_nodes_copy)
    if connexion.request.is_json:
        body = JobParams.from_dict(connexion.request.get_json())  # noqa: E501
        for job in body.jobs:
            if len(computation_nodes_copy) == 0:
                print("No computation nodes available...not completing job")
                return
            data = {'data_file': job.data_file, 'spark_program': job.spark_program}
            print(data, "data")
            computation_node = vip_to_ip[computation_nodes_copy.pop(0)]
            r = requests.post('http://%s/run_job' % computation_node, data=json.dumps(data), headers=headers)
            return r.status_code
    return 'do some magic!'
