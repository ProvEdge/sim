from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    git_uid = Column(String(50), nullable=True)
    email = Column(String(256), unique=True)
    name = Column(String(256))

class OrgUser(Base):
    __tablename__ = "org_user"
    
    org_id = Column(Integer, ForeignKey("organizations.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

# Container Cluster
# Storage Cluster
# Robot
# Instance