from os import path
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session
from app.functions import argocd_rest_crud, instance_crud
from database.schemas import argocd_schema, gitea_schema, instance_schema
from app.functions import gitea_rest_crud, robot_crud

import yaml, json, requests

class InstanceManagementResponse(BaseModel):
    status_code: int
    data: dict

def create_instance(
    base_url: str,
    access_token: str,
    body: gitea_schema.CreateInstance,
    db: Session
) -> InstanceManagementResponse:

    robot = robot_crud.get_robot(
        db=db,
        type=body.instance.robot_type
    )

    if robot is None:
        return InstanceManagementResponse(
            status_code=400,
            data={
                "msg": "Cannot find robot"
            }
        )

    user = gitea_rest_crud.get_authenticated_user(
        base_url=base_url,
        access_token=access_token
    ).data

    instances = instance_crud.get_instances(db, user_id=body.instance.user_id, robot_type=robot.type)
    if len(instances) == 0:
        fork_repo_req = gitea_rest_crud.fork_repository(
            base_url=base_url,
            access_token=access_token,
            owner=robot.base_repo_owner,
            repo=robot.base_repo_name
        )

        if fork_repo_req.status_code % 100 != 2:
            return InstanceManagementResponse(
                status_code=400,
                data={
                    "msg": "Cannot fork repo",
                    "data": fork_repo_req.data
                }
            )


    create_branch_req = gitea_rest_crud.create_branch(
        body=gitea_schema.CreateBranch(
            new_branch_name=body.instance.name,
            old_branch_name="master"
        ),
        base_url=base_url,
        access_token=access_token,
        owner=user["username"],
        repo=robot.base_repo_name
    )

    if create_branch_req.status_code == 201:
        create_file_req = gitea_rest_crud.create_file(
            body=gitea_schema.CreateFile(
                content=get_helm_values_content(body.helm)
            ),
            base_url=base_url,
            access_token=access_token,
            owner=user["username"],
            repo=robot.base_repo_name,
            branch=body.instance.name,
            filepath="my-values.yaml"
        )

        if create_file_req.status_code == 201:
            
            ins_db = instance_schema.InstanceCreate(
                name=body.instance.name,
                user_id=body.instance.user_id,
                belongs_to_group=body.instance.belongs_to_group,
                group_id=body.instance.group_id,
                cluster_id=body.instance.cluster_id,
                namespace=body.helm.namespace,
                robot_type=body.instance.robot_type,
                values_repository=robot.base_repo_name,
                values_branch=body.instance.name,
                values_path="my-values.yaml",
                argocd_project_name=body.instance.argocd_project_name
            )

            create_argo_and_save_req = create_argocd_application(
                db=db,
                argo_cluster=body.argo.argo_cluster,
                helm_path=body.argo.helm_path,
                argocd_username=user["username"],
                repo=robot.base_repo_name,
                branch=body.instance.name,
                path="my-values.yaml",
                instance=ins_db
            )

            if create_argo_and_save_req.status_code == 200:
                return InstanceManagementResponse(
                    status_code=200,
                    data=create_argo_and_save_req.data
                )
            else: return InstanceManagementResponse(
                status_code=400,
                data={
                    "msg": "Cannot create ArgoCD app",
                    "data": create_argo_and_save_req.data
                }
            )

        else: return InstanceManagementResponse(
            status_code=400,
            data={
                "msg": "Cannot create yaml file",
                "data": create_file_req.data
            }
        )

    else:
        return InstanceManagementResponse(
            status_code=400,
            data={
                "msg": "Cannot create branch for instance",
                "data": create_branch_req.data,
                "stat": create_branch_req.status_code
            }
        )


    



def create_argocd_application(
    db: Session,
    argo_cluster: str,
    helm_path: str,
    argocd_username: str,
    repo: str,
    branch: str,
    path: str,
    instance: instance_schema.InstanceCreate
) -> argocd_schema.ArgoCDResponse:

    try:
        url = argocd_schema.argocd_server_url + "/applications"
        token_res = argocd_rest_crud.get_bearer_token(
            {
                "username": "admin",
                "password": "ncHjjNs7De47HaMm"
            }
        )
        token = token_res.data["token"]
        auth_header = {
            "Cookie": "argocd.token=" + token
        }

        body = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {
                "name": instance.argocd_project_name
            },
            "spec": {
                "destination": {
                "name": "",
                "namespace": instance.namespace,
                "server": argo_cluster
                },
                "source": {
                    "path": helm_path,
                    "repoURL": gitea_schema.gitea_server + "/" + argocd_username + "/" + repo,
                    "targetRevision": branch,
                    "helm": {
                        "valueFiles": [
                        "../" + path
                        ]
                    }
                },
                "project": "default",
                "syncPolicy": {
                    "automated": {
                        "prune": False,
                        "selfHeal": True
                    }
                }
            }
        }

        response =  requests.post(url=url, headers=auth_header, data=json.dumps(body), verify=False)
        status_code = response.status_code
        data = response.json()

        instance_db = {}
        if status_code == 200:
            instance_db = instance_crud.create_instance(db, instance)

        return argocd_schema.ArgoCDResponse(
            status_code=status_code,
            data={
                "instance": instance_db,
                "argocd": data
            }
        )
    except Exception as e:
        # clear all
        return argocd_schema.ArgoCDResponse(
            status_code=0,
            data={
                "message": str(e)
            }
        )
        
   




def get_helm_values_content(values: gitea_schema.HelmValues):
    values_json = {
        "namespace": values.namespace,
        "cmStartName": values.cm_start_name,
        "cmSupervisordName": values.cm_supervisord_name,
        "deploymentName": values.dep_name,
        "deploymentReplicas": values.replicas,
        "httpPort": values.http_port,
        "webrtcPort": values.webrtc_port,
        "theiaPort": values.theia_port,
        "rosbridgePort": values.rosbridge_port,
        "webvizPort": values.webviz_port
    }

    values_yaml = yaml.dump(values_json, allow_unicode=True)
    return values_yaml