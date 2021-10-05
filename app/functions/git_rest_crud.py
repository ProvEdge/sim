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
    
def edit_helm_values(access_token: str, repo_name: str, filepath: str, values_content: git_schema.HelmValues) -> git_schema.GitResponse:
    try:
        g = Github(access_token)

        repo = g.get_repo(repo_name)

        edit_file = repo.update_file(
            path=filepath,
            message=filepath + " is updated",
            content=get_helm_values_content(values_content)
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

def get_helm_values_content(values: git_schema.HelmValues) -> str:
    
    gmt = time.gmtime()
    ts = str(calendar.timegm(gmt))

    values_json = {
        "namespace": values.namespace,
        "cmStartName": values.cm_start_name + "-" + ts,
        "cmSupervisordName": values.cm_supervisord_name + "-" + ts,
        "deploymentName": values.dep_name + "-" + ts,
        "deploymentReplicas": values.replicas,
        "httpPort": values.http_port,
        "webrtcPort": values.webrtc_port,
        "theiaPort": values.theia_port,
        "rosbridgePort": values.rosbridge_port,
        "webvizPort": values.webviz_port
    }

    values_yaml = yaml.dump(values_json, allow_unicode=True)

    return values_yaml