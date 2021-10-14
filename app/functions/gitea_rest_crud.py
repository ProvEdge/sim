
from giteapy.models.create_file_options import CreateFileOptions
from giteapy.models.create_user_option import CreateUserOption
from giteapy.models.edit_repo_option import EditRepoOption
from giteapy.models.update_file_options import UpdateFileOptions
from app.functions.general_functions import gitea_admin_api, gitea_repo_api, gitea_user_api

from giteapy.models.create_repo_option import CreateRepoOption
from giteapy.models.create_file_options import CreateFileOptions
from giteapy.models.create_key_option import CreateKeyOption


from database.schemas import gitea_schema

import base64, requests, json

def prepare_auth_header(token: str):
    return {
        "Authorization": "Bearer " + token
    }


def get_authenticated_user(base_url: str, access_token: str) -> gitea_schema.GiteaResponse:

    url = base_url + "/user"

    r = requests.get(
        url=url,
        headers=prepare_auth_header(access_token)
    )

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=r.json()
    )

def get_repository(base_url: str, access_token: str, owner: str, repo: str):
    
    url = base_url + "/repos/" + owner + "/" + repo

    r = requests.get(
        url=url,
        headers=prepare_auth_header(access_token)
    )

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=r.json()
    )

def fork_repository(base_url: str, access_token: str, owner: str, repo: str):
    
    url = base_url + "/repos/" + owner + "/" + repo + "/forks"
    
    body = {"": ""}

    r = requests.post(
        url=url,
        headers=prepare_auth_header(access_token),
        data=body
    )

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=r.json()
    )

def get_branches(base_url: str, access_token: str, owner: str, repo: str):
    
    url = base_url + "/repos/" + owner + "/" + repo + "/branches"
    
    r = requests.get(
        url=url,
        headers=prepare_auth_header(access_token),
    )

    # returns array
    branches = {
        "branches": r.json()
    }

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=branches
    )


def create_branch(body: gitea_schema.CreateBranch, base_url: str, access_token: str, owner: str, repo: str):
    
    url = base_url + "/repos/" + owner + "/" + repo + "/branches"

    r = requests.post(
        url=url,
        headers=prepare_auth_header(access_token),
        json=body.dict()
    )

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=r.json()
    )


def delete_branch(base_url: str, access_token: str, owner: str, repo: str, branch: str):
    
    url = base_url + "/repos/" + owner + "/" + repo + "/branches/" + branch
    
    r = requests.delete(
        url=url,
        headers=prepare_auth_header(access_token),
    )

    data = {}

    if r.status_code != 204:
        data = r.json()

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=data
    )


def get_file_content(base_url: str, access_token: str, owner: str, repo: str, branch: str, filepath: str):

    url = base_url + "/repos/" + owner + "/" + repo + "/contents/" + filepath
    
    r = requests.get(
        url=url,
        headers=prepare_auth_header(access_token),
        params={
            "ref": branch
        }
    )

    # returns array
    content = {
        "content": r.json()
    }

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=content
    )

# def change_repo_name(base_url: str, access_token: str, owner: str, repo: str, new_name: str):
#     repo_api = gitea_repo_api(
#         url=base_url,
#         access_token=access_token
#     )

#     change_name = repo_api.repo_edit(
#         owner=owner,
#         repo=repo,
#         body=EditRepoOption(
#             name=new_name
#         )
#     )

#     return change_name


# def create_repository(base_url: str, access_token: str, data: gitea_schema.CreateRepository) -> gitea_schema.GiteaResponse:
#     try:
#         api_instance = gitea_repo_api(
#             url=base_url,
#             access_token=access_token
#         )

#         new_repo = api_instance.create_current_user_repo(
#             body=CreateRepoOption(
#                 auto_init=True,
#                 name=data.name,
#                 private=False # True in future
#             )
#         )

#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "new_repo": new_repo
#             }
#         )

#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 "from_service": new_repo
#             }
#         )

# def delete_repository(base_url: str, access_token: str, owner: str, repo: str):
#     repo_api = gitea_repo_api(
#         url=base_url,
#         access_token=access_token
#     )

#     return repo_api.repo_delete(
#         owner=owner,
#         repo=repo
#     )
    
# def get_file_content(base_url: str, access_token: str, owner: str, repo: str, filepath: str) -> gitea_schema.GiteaResponse:
#     try:
#         api_instance = gitea_repo_api(
#             url=base_url,
#             access_token=access_token
#         )

#         content = api_instance.repo_get_contents(
#             owner=owner,
#             repo=repo,
#             filepath=filepath
#         )


#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "content": base64_to_str(content.content)
#             }
#         )
#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": content
#             }
#         )

# def create_file(data: gitea_schema.CreateFile, base_url: str, access_token: str, owner: str, repo: str, filepath: str) -> gitea_schema.GiteaResponse:
#     try:
#         api_instance = gitea_repo_api(
#             url=base_url,
#             access_token=access_token
#         )
        
#         content_base64 = str_to_base64(data.content)

#         new_file = api_instance.repo_create_file(
#             owner=owner,
#             repo=repo,
#             filepath=filepath,
#             body=CreateFileOptions(
#                 content=content_base64,
#                 message=filepath + " is created",
#                 branch="main"
#             )
#         )

#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "content": new_file
#             }
#         )
#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": new_file
#             }
#         )



# def update_file(data: gitea_schema.UpdateFile, base_url: str, access_token: str, owner: str, repo: str, filepath: str) -> gitea_schema.GiteaResponse:
#     try:
#         api_instance = gitea_repo_api(
#             url=base_url,
#             access_token=access_token
#         )
        
#         content_base64 = str_to_base64(data.content)

#         file_content = api_instance.repo_get_contents(
#             owner=owner,
#             repo=repo,
#             filepath=filepath
#         )

#         new_file_version = api_instance.repo_update_file(
#             owner=owner,
#             repo=repo,
#             filepath=filepath,
#             body=UpdateFileOptions(
#                 content=content_base64,
#                 message=filepath + " is updated",
#                 branch="main",
#                 sha=file_content.sha
#             )
#         )

        

#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "content": new_file_version
#             }
#         )
#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": new_file
#             }
#         )


# ### ADMIN API ###

# def create_user(user: gitea_schema.CreateUser, base_url: str, admin_access_token: str):
#     try:
#         api_instance = gitea_admin_api(
#             url=base_url,
#             access_token=admin_access_token
#         )

#         new_user = api_instance.admin_create_user(
#             body=CreateUserOption(
#                 email=user.email,
#                 full_name=user.full_name,
#                 login_name=user.login_name,
#                 must_change_password=False,
#                 password=user.password,
#                 send_notify=False,
#                 username=user.username
#             )
#         )

#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "user": new_user
#             }
#         )
#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": new_file
#             }
#         )


# def get_users(base_url: str, admin_access_token: str):
#     try:
#         api_instance = gitea_admin_api(
#             url=base_url,
#             access_token=admin_access_token
#         )

#         users = api_instance.admin_get_all_users()

#         return gitea_schema.GiteaResponse(
#             is_successful=True,
#             data={
#                 "users": users
#             }
#         )
#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": new_file
#             }
#         )

# def create_public_key(username: str, base_url: str, admin_access_token: str):
#     try:
#         api_instance = gitea_admin_api(
#             url=base_url,
#             access_token=admin_access_token
#         )

#     except Exception as e:
#         return gitea_schema.GiteaResponse(
#             is_successful=False,
#             data={
#                 "msg": str(e),
#                 #"from_service": new_file
#             }
#         )

# def base64_to_str(base64_str: str):
#     return base64.b64decode(base64_str).decode('utf-8')

# def str_to_base64(s: str):
#     return base64.b64encode(s.encode('utf-8')).decode('utf-8')