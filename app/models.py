from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from database.database import Base

# user_id
# group_id

class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    api_server_address = Column(String(50), nullable=False)
    group_id = Column(String(100), nullable=False) # coming from Keycloak
    
    __table_args__ = (
        UniqueConstraint('api_server_address', 'group_id', name='address_group_uc'),
    )


class Storage(Base):
    __tablename__ = "storages"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    pvc_name = Column(String(100), nullable=False)
    pv_name = Column(String(100), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('cluster_id', 'pvc_name', name="cluster_pvc_uv"),
        UniqueConstraint('cluster_id', 'pv_name', name="cluster_pv_uv"),
    )

class Robot(Base):
    __tablename__ = "robots"
    
    type = Column(String(100), primary_key=True, unique=True)
    has_gpu = Column(Boolean, nullable=False)
    gpu_mb = Column(Integer, nullable=True)
    cpu_mb = Column(Integer, nullable=False)
    ram_mb = Column(Integer, nullable=False)

class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False) # keycloak foreign key
    belongs_to_group = Column(Boolean, nullable=False)
    group_id = Column(String(100), nullable=False) # keycloak foreign key
    cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    #storage_id = Column(Integer, ForeignKey("storages.id"), nullable=False)
    namespace = Column(String(100), nullable=False)
    deployment = Column(String(100), nullable=False)
    robot_type = Column(String, ForeignKey("robots.type"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('cluster_id', 'namespace', 'deployment', name="cluster_ns_dep_uc"),
        UniqueConstraint('user_id', 'name', name="user_id_instance_name_uc"),
    )





# class Organization(Base):
#     __tablename__ = "organizations"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)

# class User(Base):
#     __tablename__ = "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     git_uid = Column(String(50), nullable=True)
#     email = Column(String(256), unique=True)
#     name = Column(String(256))

# class OrgUser(Base):
#     __tablename__ = "org_user"
    
#     org_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

# Container Cluster
# Storage Cluster
# Robot
# Instance