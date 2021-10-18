
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


def delete_repository(base_url: str, access_token: str, owner: str, repo: str):
    
    url = base_url + "/repos/" + owner + "/" + repo

    r = requests.delete(
        url=url,
        headers=prepare_auth_header(access_token)
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


def create_branch(body: gitea_schema.CreateBranch, base_url: str, access_token: str, owner: str, repo: str) -> gitea_schema.GiteaResponse:
    
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

    content = {}

    if r.status_code == 200:
        # may return array
        content = {
            "content": base64_to_str(r.json()["content"]),
            "sha": r.json()["sha"]
        }
    else: content = r.json()

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=content
    )


def create_file(body: gitea_schema.CreateFile, base_url: str, access_token: str, owner: str, repo: str, branch: str, filepath: str):

    url = base_url + "/repos/" + owner + "/" + repo + "/contents/" + filepath

    req_body = {
        "branch": branch,
        "content": str_to_base64(body.content),
        "message": filepath + " is created",
        "signoff": True
    }

    r = requests.post(
        url=url,
        headers=prepare_auth_header(access_token),
        json=req_body
    )

    data = {}

    if r.status_code == 201:
        data = {
            "content": base64_to_str(r.json()["content"]["content"]),
            "commit_url": r.json()["commit"]["url"],
            "commit_message": r.json()["commit"]["message"]
        }

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=data
    )



def update_file_content(body: gitea_schema.UpdateFile, base_url: str, access_token: str, owner: str, repo: str, branch: str, filepath: str):

    url = base_url + "/repos/" + owner + "/" + repo + "/contents/" + filepath

    file_content_req = get_file_content(
        owner=owner,
        repo=repo,
        branch=branch,
        filepath=filepath,
        base_url=base_url,
        access_token=access_token
    )

    if file_content_req.status_code != 200:
        return gitea_schema.GiteaResponse(
            status_code=file_content_req.status_code,
            data=file_content_req.data
        )

    file_sha = file_content_req.data["sha"]

    req_body = {
        "branch": branch,
        "content": str_to_base64(body.content),
        "message": filepath + " is updated",
        "sha": file_sha,
        "signoff": True
    }


    r = requests.put(
        url=url,
        headers=prepare_auth_header(access_token),
        json=req_body
    )

    data = {}

    if r.status_code == 200:
        data = {
            "content": base64_to_str(r.json()["content"]["content"]),
            "commit_url": r.json()["commit"]["url"],
            "commit_message": r.json()["commit"]["message"]
        }

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=data
    )



def delete_file(base_url: str, access_token: str, owner: str, repo: str, branch: str, filepath: str):

    url = base_url + "/repos/" + owner + "/" + repo + "/contents/" + filepath

    file_content_req = get_file_content(
        owner=owner,
        repo=repo,
        branch=branch,
        filepath=filepath,
        base_url=base_url,
        access_token=access_token
    )

    if file_content_req.status_code != 200:
        return gitea_schema.GiteaResponse(
            status_code=file_content_req.status_code,
            data=file_content_req.data
        )

    file_sha = file_content_req.data["sha"]

    req_body = {
        "branch": branch,
        "message": filepath + " is deleted",
        "sha": file_sha,
        "signoff": True
    }

    r = requests.delete(
        url=url,
        headers=prepare_auth_header(access_token),
        json=req_body
    )

    print(r.json())

    data = {}

    if r.status_code == 200:
        data = {
            "commit_url": r.json()["commit"]["url"],
            "commit_message": r.json()["commit"]["message"]
        }

    return gitea_schema.GiteaResponse(
        status_code=r.status_code,
        data=data
    )


def base64_to_str(base64_str: str):
    return base64.b64decode(base64_str).decode('utf-8')

def str_to_base64(s: str):
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')