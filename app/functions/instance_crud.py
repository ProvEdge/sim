from sqlalchemy.orm import Session

from .. import models
from database.schemas import instance_schema, keycloak_schema
from app.functions.general_functions import authorize

def get_instances(db: Session, user_id: str="", belongs_to_group: bool=False, group_id: str="", cluster_id: int=0, robot_type: str="", skip: int = 0, limit: int = 100):
    instances = db.query(models.Instance)
    if user_id != "":
        instances = instances.filter(models.Instance.user_id == user_id)
    if belongs_to_group and group_id != "":
        instances = instances.filter(models.Instance.belongs_to_group == belongs_to_group, models.Instance.group_id == group_id)
    if cluster_id != 0:
        instances = instances.filter(models.Instance.cluster_id == cluster_id)
    if robot_type != "":
        instances = instances.filter(models.Instance.robot_type == robot_type)

    return instances.offset(skip).limit(limit).all()

def get_instance(
    db: Session, 
    id: int,
    credentials: keycloak_schema.Credentials,
):
    return db.query(models.Instance).filter(
        models.Instance.id == id,
        models.Instance.user_id == credentials.user_id
    ).first()


def get_instance_by_name(
    db: Session, 
    name: str,
    credentials: keycloak_schema.Credentials,
):
    return db.query(models.Instance).filter(
        models.Instance.name == name,
        models.Instance.user_id == credentials.user_id
    ).first()

# def get_clusters_by_group_id(db: Session, group_id: str):
#     return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_instance(
    db: Session, 
    instance: instance_schema.InstanceCreate,
    credentials: keycloak_schema.Credentials,
):
    db_instance = models.Instance(
        name=instance.name,
        user_id=credentials.user_id,
        # belongs_to_group=instance.belongs_to_group,
        # group_id=instance.group_id,
        # cluster_id=instance.cluster_id,
        namespace=instance.namespace,
        robot_type=instance.robot_type,
        release_name=instance.release_name,
        helm_values=instance.helm_values
    )
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance

def edit_instance(
    db: Session, id: int, 
    instance: instance_schema.InstanceEdit,
    credentials: keycloak_schema.Credentials
):
    attributes = {}
    for attr, value in instance.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.Instance).filter(
        models.Instance.id == id, 
        models.Instance.user_id == credentials.user_id
    ).update(attributes)

    db.commit()
    db_instance = get_instance(db, id)
    return db_instance

def delete_instance(
    db: Session, 
    id: int,
    credentials: keycloak_schema.Credentials
):
    db_instance = get_instance(
        db=db, 
        id=id,
        credentials=credentials
        )
    query_exec = db.query(models.Instance).filter(
        models.Instance.id == id,
        models.Instance.user_id == credentials.user_id
    ).delete()
    
    print(str(query_exec))
    db.commit()
    return db_instance