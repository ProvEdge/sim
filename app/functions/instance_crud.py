from sqlalchemy.orm import Session

from .. import models
from database.schemas import instance_schema

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

def get_instance(db: Session, id: int):
    return db.query(models.Instance).filter(models.Instance.id == id).first()

# def get_clusters_by_group_id(db: Session, group_id: str):
#     return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_instance(db: Session, instance: instance_schema.InstanceCreate):
    db_instance = models.Instance(
        name=instance.name,
        user_id=instance.user_id,
        # belongs_to_group=instance.belongs_to_group,
        # group_id=instance.group_id,
        # cluster_id=instance.cluster_id,
        namespace=instance.namespace,
        robot_type=instance.robot_type,
    )
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance

def edit_instance(db: Session, id: int, instance: instance_schema.InstanceEdit):
    attributes = {}
    for attr, value in instance.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.Instance).filter(models.Instance.id == id).update(attributes)
    db.commit()
    db_instance = get_instance(db, id)
    return db_instance

def delete_instance(db: Session, id: int):
    db_instance = get_instance(db, id)
    query_exec = db.query(models.Instance).filter(models.Instance.id == id).delete()
    print(str(query_exec))
    db.commit()
    return db_instance