from fastapi import Depends
import prefect
from prefect import task, Flow, Parameter
import requests
from requests.api import request

from sqlalchemy.orm.session import Session
from app.functions.general_functions import get_db
  
from app.functions import kubeapps_rest_crud, robot_crud
from app.versions.v0.routes import robots
from database.schemas import kubeapps_schema, keycloak_schema, robot_schema

# @task
# def say_hello():
#     logger = prefect.context.get("logger")
#     logger.info("Hello, Cloud!")
    
# @task
# def say_goodbye():
#     logger = prefect.context.get("logger")
#     logger.info("Goodbye, Cloud!")
    
@task(name="get_robot")
def get_robot(
    robot_type: str,
):
    
    req = requests.get(url="http://localhost:8000/api/v0/sim/robots/" + robot_type)
    resp = req.json()
    robot = resp["data"]
    robot_obj = robot_schema.Robot.parse_obj(robot)
    
    logger = prefect.context.get("logger")
    logger.info(str(resp))
    
    return robot_obj
    
    
    
    
    
@task(name="create_kubeapps_release")
def create_kubeapps_release_task(
    identity: dict,
    name: str,
    robot: robot_schema.Robot,
):
    
    logger = prefect.context.get("logger")
    logger.info(str(robot))
    logger.info(str(robot.app_repository_namespace))
    
    
    req = kubeapps_rest_crud.post_release_v2(
        id_token=identity["id_token"],
        namespace=identity["username"],
        release=kubeapps_schema.CreateRelease(
            appRepositoryResourceName=robot.app_repository,
            appRepositoryResourceNamespace=robot.app_repository_namespace,
            chartName=robot.chart_name,
            version=robot.chart_version,
            releaseName=name,
            values=manipulate_values_v2(
                helm_values=robot.helm_values,
                identity=identity
            )
        ).dict()
    )
    
    logger = prefect.context.get("logger")
    logger.info(str(req))
    



# replace it with smarter helm value picker !
def manipulate_values_v2(helm_values: str, identity: dict):
    import yaml
    received_yaml = yaml.safe_load(helm_values)
    received_yaml["namespace"] = identity["username"]
    converted_yaml = yaml.dump(received_yaml, allow_unicode=True)
    return converted_yaml


def create_flow():
    
    with Flow("eskaza") as flow:
        identity = Parameter('identity', default={})
        name = Parameter('name', default="default_name")
        robot_type = Parameter('robot_type', default="default_robot_type")
        
        robot = get_robot(
            robot_type=robot_type
        )
        
        create_kubeapps_release_task(
            identity=identity,
            name=name,
            robot=robot
        )
        
    # Register the flow under the "tutorial" project
    flow.register(project_name="tunahan")