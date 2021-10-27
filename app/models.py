from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint, DateTime, CheckConstraint, Float
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import column

from database.database import Base

# user_id
# group_id

# class Cluster(Base):
#     __tablename__ = "clusters"

#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     api_server_address = Column(String(50), nullable=False)
#     group_id = Column(String(100), nullable=False) # coming from Keycloak
    
#     __table_args__ = (
#         UniqueConstraint('api_server_address', 'group_id', name='address_group_uc'),
#     )


# class Storage(Base):
#     __tablename__ = "storages"

#     id = Column(Integer, primary_key=True, index=True, unique=True)
#     cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
#     pvc_name = Column(String(100), nullable=False)
#     pv_name = Column(String(100), nullable=False)
    
#     __table_args__ = (
#         UniqueConstraint('cluster_id', 'pvc_name', name="cluster_pvc_uv"),
#         UniqueConstraint('cluster_id', 'pv_name', name="cluster_pv_uv"),
#     )

class Robot(Base):
    __tablename__ = "robots"
    
    type = Column(String(100), primary_key=True, unique=True)
    has_gpu = Column(Boolean, nullable=False)
    gpu_mb = Column(Integer, nullable=True)
    cpu_mb = Column(Integer, nullable=False)
    ram_mb = Column(Integer, nullable=False)
    app_repository = Column(String, nullable=False)
    app_repository_namespace = Column(String, nullable=False)
    chart_name = Column(String, nullable=False)
    chart_version = Column(String, nullable=False)
    helm_values = Column(String, nullable=False)

class Instance(Base):
    __tablename__ = "instances"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(String(100), nullable=False) # keycloak foreign key
    # belongs_to_group = Column(Boolean, nullable=False)
    # group_id = Column(String(100), nullable=False) # keycloak foreign key
    # cluster_id = Column(Integer, ForeignKey("clusters.id"), nullable=False)
    namespace = Column(String(100), nullable=False)
    robot_type = Column(String, ForeignKey("robots.type"), nullable=False)
    helm_values = Column(String, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name="user_id_instance_name_uc"),
    )

class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    start_time = Column(DateTime, nullable=False, default=datetime.now())
    end_time = Column(DateTime, nullable=True)
    is_terminated = Column(Boolean, nullable=False, default=False)

    # deep copy of the instance
    ins_id = Column(Integer, nullable=False)
    ins_name = Column(String(100), nullable=False)
    ins_user_id = Column(String(100), nullable=False) # keycloak foreign key
    # ins_belongs_to_group = Column(Boolean, nullable=False)
    # ins_group_id = Column(String(100), nullable=False) # keycloak foreign key
    # ins_cluster_id = Column(Integer, nullable=False)
    ins_namespace = Column(String(100), nullable=False)
    ins_robot_type = Column(String, nullable=False)
    ins_helm_values = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint('start_time <= end_time', 'start_end_time_consistency'),
    )

# class Bill(Base):
#     __tablename__ = "bills"
    
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     usage_id = Column(Integer, ForeignKey("usages.id"), nullable=False, unique=True)
#     amount = Column(Float, nullable=False)
#     currency = Column(String, nullable=False)
#     is_paid = Column(Boolean, nullable=False, default=False)

#     __table_args__ = (
#         CheckConstraint(name="currency_options_cc", sqltext="currency = 'USD' OR currency = 'TL'"),
#     )

# class PricingFormula(Base):
#     __tablename__ = "pricing_formulas"

#     name = Column(String, primary_key=True)
#     robot_type = Column(String, ForeignKey("robots.type"), nullable=False)
#     robot_coefficient = Column(Float, nullable=False)
#     time_unit = Column(String, nullable=False)
#     amount_per_time_unit = Column(Float, nullable=False)
#     currency = Column(String, nullable=False)

#     __table_args__ = (
#         CheckConstraint(name="currency_options_cc", sqltext="currency = 'USD' OR currency = 'TL'"),
#     )

# class Transaction(Base):
#     __tablename__ = "transactions"

#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
#     usage_id = Column(Integer, ForeignKey("usages.id"), nullable=False, unique=True)
#     bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False, unique=True)
#     method = Column(String, nullable=False)
#     details = Column(String, nullable=False)