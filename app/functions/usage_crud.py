from app.functions import instance_crud
from datetime import datetime
from sqlalchemy.orm import Session

from .. import models
from database.schemas import usage_schema

def get_usages(db: Session, start_time: datetime = "", end_time: datetime = "", is_terminated: bool = True, ins_user_id: str = "", ins_belongs_to_group: bool = False, ins_group_id: str = "", ins_cluster_id: int = 0, ins_robot_type: str = "", ins_id: int = 0, skip: int = 0, limit: int = 100):
    usages = db.query(models.Usage)
    if start_time != "":
        usages = usages.filter(models.Usage.start_time > start_time)
    if end_time != "":
        usages = usages.filter(models.Usage.end_time > end_time)
    if ins_user_id != "":
        usages = usages.filter(models.Usage.ins_user_id == ins_user_id)
    if ins_belongs_to_group and ins_group_id != "":
        usages = usages.filter(models.Usage.ins_group_id == ins_group_id)
    if ins_cluster_id != 0:
        usages = usages.filter(models.Usage.ins_cluster_id == ins_cluster_id)
    if ins_robot_type != "":
        usages = usages.filter(models.Usage.ins_robot_type == ins_robot_type)
    if ins_id != 0:
        usages = usages.filter(models.Usage.ins_id == ins_id)
        
    usages = usages.filter(models.Usage.is_terminated == is_terminated)

    return usages.offset(skip).limit(limit).all()

def get_usage(db: Session, id: int):
    return db.query(models.Usage).filter(models.Usage.id == id).first()

def create_usage(db: Session, usage: usage_schema.UsageCreate):
    db_instance = instance_crud.get_instance(db, usage.instance_id)

    db_usage = models.Usage(
        # start_time=usage.start_time,
        # end-time is null
        is_terminated=False,
        ins_id=db_instance.id,
        ins_name=db_instance.name,
        ins_user_id=db_instance.user_id,
        ins_belongs_to_group=db_instance.belongs_to_group,
        ins_group_id=db_instance.group_id,
        ins_cluster_id=db_instance.cluster_id,
        ins_namespace=db_instance.namespace,
        #ins_deployment=db_instance.deployment,
        #ins_service=db_instance.service,
        #ins_configmaps=db_instance.configmaps,
        ins_robot_type=db_instance.robot_type,
        ins_values_repository=db_instance.values_repository,
        ins_values_branch=db_instance.values_branch,
        ins_values_path=db_instance.values_path,
        ins_argocd_project_name=db_instance.argocd_project_name
    )

    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    return db_usage

def edit_usage(db: Session, id: int, usage: usage_schema.UsageEdit):
    attributes = {}
    for attr, value in usage.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.Usage).filter(models.Usage.id == id).update(attributes)
    db.commit()
    db_usage = get_usage(db, id)
    return db_usage

def delete_usage(db: Session, id: int):
    db_usage = get_usage(db, id)
    query_exec = db.query(models.Usage).filter(models.Usage.id == id).delete()
    db.commit()
    return db_usage