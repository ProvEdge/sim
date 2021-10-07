import json
from typing import Union
import yaml, time, calendar

from github import Github

from database.schemas import git_schema


def add_instance_values(access_token: str, repo_name: str, filepath: str, values_content: git_schema.HelmValues) -> git_schema.GitResponse:
    try:
        g = Github(access_token)

        repo = g.get_repo(repo_name)

        create_file = repo.create_file(
            path=filepath,
            message="new file via python",
            content=get_helm_values_content(values_content)
        )

        file_content = g.get_repo(repo_name).get_contents(filepath).decoded_content
       
        return git_schema.GitResponse(
            is_successful=True,
            data={
                "message": "Git request is successful",
                "values": {
                    "filepath": filepath,
                    "content": file_content
                }
            }
        )
    except Exception as e:
        return git_schema.GitResponse(
            is_successful=False,
            data={
                "message": str(e)
            }
        )
    


def edit_helm_values(access_token: str, repo_name: str, filepath: str, values_content: git_schema.EditHelmValues) -> git_schema.GitResponse:
    try:

        g = Github(access_token)
        repo = g.get_repo(repo_name)
        sha_value = repo.get_contents(filepath).sha
        content = repo.get_contents(filepath).decoded_content

        cnt = yaml.safe_load(content)
        cnt_json_str = json.dumps(cnt)
        cnt_json = json.loads(cnt_json_str)

        new_values_json = helm_obj_to_json(values_content)

        for key in new_values_json:
            if new_values_json[key] is None: continue
            else:
                if new_values_json[key] != cnt_json[key]:
                    cnt_json[key] = new_values_json[key]
        
        edit_file = repo.update_file(
            path=filepath,
            message=filepath + " is updated",
            content=helm_json_to_yaml(cnt_json),
            sha=sha_value
        )

        return git_schema.GitResponse(
            is_successful=True,
            data={
                "message": "Git request is successful"
            }
        )
    except Exception as e:
        return git_schema.GitResponse(
            is_successful=False,
            data={
                "message": str(e)
            }
        )


def delete_helm_values(access_token: str, repo_name: str, filepath: str) -> git_schema.GitResponse:
    try:

        g = Github(access_token)
        repo = g.get_repo(repo_name)

        sha_value = repo.get_contents(filepath).sha
        
        delete_file = repo.delete_file(
            path=filepath,
            message=filepath + " is deleted",
            sha=sha_value
        )

        return git_schema.GitResponse(
            is_successful=True,
            data={
                "message": "Git request is successful"
            }
        )
    except Exception as e:
        return git_schema.GitResponse(
            is_successful=False,
            data={
                "message": str(e)
            }
        )

def get_commits(access_token: str, repo_name: str, filepath: str):
    g = Github(access_token)
    repo = g.get_repo(repo_name)

    commits = repo.get_commits(
        path=filepath
    )

    for c in commits:
        print("----------------")
        for f in c.files:
            if f.filename == filepath:
                print(find_line_and_jsonify("deploymentReplicas:", f.patch), "///",  c.commit.author.date)

    return {
        "msg": "to be logged"
    }


def get_helm_values_content(values: git_schema.HelmValues):
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

def helm_obj_to_json(values: git_schema.HelmValues):
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

    return values_json

def helm_json_to_yaml(values: dict):
    values_yaml = yaml.dump(values, allow_unicode=True)
    return values_yaml

def find_line_and_jsonify(attribute: str, data: str):
    lines = data.split(sep="\n")
    for l in lines:
        if attribute in l:
            return l
    return "not found"