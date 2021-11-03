from typing import List
from sqlalchemy.orm import Session

from .. import models
from database.schemas import robot_schema

def get_robots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Robot).offset(skip).limit(limit).all()
    

def get_robot(db: Session, type: str):
    return db.query(models.Robot).filter(models.Robot.type == type).first()

# def get_clusters_by_group_id(db: Session, group_id: str):
#     return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_robot(db: Session, robot: robot_schema.RobotCreate):
    db_robot = models.Robot(
        type=robot.type,
        has_gpu=robot.has_gpu,
        gpu_mb=robot.gpu_mb,
        cpu_mb=robot.cpu_mb,
        ram_mb=robot.ram_mb,
        app_repository=robot.app_repository,
        app_repository_namespace=robot.app_repository_namespace,
        chart_name=robot.chart_name,
        chart_version=robot.chart_version,
        helm_values=robot.helm_values
    )
    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot

def edit_robot(db: Session, type: str, robot: robot_schema.RobotEdit):
    attributes = {}
    for attr, value in robot.__dict__.items():
        if value is not None:
            attributes[attr] = value

    db.query(models.Robot).filter(models.Robot.type == type).update(attributes)
    db.commit()
    if robot.type is not None:
        db_robot = get_robot(db, robot.type)
    else: db_robot = get_robot(db, type)
    return db_robot

def delete_robot(db: Session, type: str):
    db_robot = get_robot(db, type)
    query_exec = db.query(models.Robot).filter(models.Robot.type == type).delete()
    db.commit()
    return db_robot