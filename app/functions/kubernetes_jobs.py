import os, json, requests, yaml
from kubernetes import client
from typing import Union

from app.functions import general_functions
from database.schemas import generic, platform_schema

def apply_configmaps(robot: str, namespace: str, APIServer: str, Token: str) -> Union[dict,str,platform_schema.K8sResponse]:
    with open(os.path.dirname(os.path.abspath(__file__))+'/../static/json/instance_repositories.json') as json_content:
        yamls = json.load(json_content)
        robot_github_start_cm_link = yamls["robots"][robot]["configmaps"]["start"]
        robot_github_supervisord_cm_link = yamls["robots"][robot]["configmaps"]["supervisord"]
        robot_github_start_cm = requests.get(robot_github_start_cm_link).text
        robot_github_supervisord_cm = requests.get(robot_github_supervisord_cm_link).text

        # KUBERNETES CONFIG
        api_client = general_functions.get_k8s_api_client(host_url=APIServer, bearer_token=Token)
        api_core = client.CoreV1Api(api_client)

        received_yaml_start = yaml.safe_load(robot_github_start_cm)
        received_json_str_start = json.dumps(received_yaml_start)
        received_json_start = json.loads(received_json_str_start)

        received_yaml_supervisord = yaml.safe_load(robot_github_supervisord_cm)
        received_json_str_supervisord = json.dumps(received_yaml_supervisord)
        received_json_supervisord = json.loads(received_json_str_supervisord)


        k8s_response_start = api_core.create_namespaced_config_map(
            namespace=namespace,
            body=received_json_start
        )

        k8s_response_supervisord = api_core.create_namespaced_config_map(
            namespace=namespace,
            body=received_json_supervisord
        )

        return {
            "start": k8s_response_start.to_dict(),
            "supervisord": k8s_response_supervisord.to_dict()
        }


def apply_deployment(robot: str, namespace):
    return ""

