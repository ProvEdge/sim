from sqlalchemy.orm import Session

from .. import models
from database.schemas import cluster_schema

def get_clusters(db: Session, group_id: str, api_server_address: str, skip: int = 0, limit: int = 100):
    clusters = db.query(models.Cluster)
    if group_id != "":
        clusters = clusters.filter(models.Cluster.group_id == group_id)
    if api_server_address != "":
        clusters = clusters.filter(models.Cluster.api_server_address == api_server_address)
    return clusters.offset(skip).limit(limit).all()

def get_cluster(db: Session, id: int):
    return db.query(models.Cluster).filter(models.Cluster.id == id).first()

def get_clusters_by_group_id(db: Session, group_id: str):
    return db.query(models.Cluster).filter(models.Cluster.group_id == group_id).all()

def create_cluster(db: Session, cluster: cluster_schema.ClusterCreate):
    db_cluster = models.Cluster(
        api_server_address=cluster.api_server_address,
        group_id =cluster.group_id
    )
    db.add(db_cluster)
    db.commit()
    db.refresh(db_cluster)
    return db_cluster

def edit_cluster(db: Session, id: int, cluster: cluster_schema.ClusterEdit):
    attributes = {}
    for attr, value in cluster.__dict__.items():
        if value is not None:
            attributes[attr] = value

    print(attributes)
    db.query(models.Cluster).filter(models.Cluster.id == id).update(attributes)
    db.commit()
    db_cluster = get_cluster(db, id)
    return db_cluster

def delete_cluster(db: Session, id: int):
    db_cluster = get_cluster(db, id)
    query_exec = db.query(models.Cluster).filter(models.Cluster.id == id).delete()
    db.commit()
    return db_cluster