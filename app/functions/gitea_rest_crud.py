
from giteapy.models.create_file_options import CreateFileOptions
from app.functions.general_functions import gitea_repo_api

from giteapy.models.create_repo_option import CreateRepoOption
from database.schemas import gitea_schema



def get_repository(url: str, access_token: str, owner: str, repo: str):
    repo_api = gitea_repo_api(
        url=url,
        access_token=access_token
    )

    return repo_api.repo_get(
        owner=owner,
        repo=repo
    )

def create_repository(base_url: str, access_token: str, data: gitea_schema.CreateRepository) -> gitea_schema.GiteaResponse:
    try:
        api_instance = gitea_repo_api(
            url=data.base_url,
            access_token=data.access_token
        )

        new_repo = api_instance.create_current_user_repo(
            body=CreateRepoOption(
                auto_init=True,
                name=data.name,
                private=False # True in future
            )
        )

        return gitea_schema.GiteaResponse(
            is_successful=True,
            data={
                "new_repo": new_repo
            }
        )

    except Exception as e:
        return gitea_schema.GiteaResponse(
            is_successful=False,
            data={
                "msg": str(e),
                "from_service": new_repo
            }
        )

    

    