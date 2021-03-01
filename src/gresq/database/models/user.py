from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func, text, and_
from sqlalchemy.sql import exists
from sqlalchemy.schema import Table
from sqlalchemy.dialects.postgresql import *


from gresq.database import Base, class_registry

role_association_table = Table('role_association', Base.metadata,
    Column('username', Integer, ForeignKey('user.username')),
    Column('role_name', Integer, ForeignKey('role.role_name'))
)
group_association_table = Table('group_association', Base.metadata,
    Column('username', Integer, ForeignKey('user.username')),
    Column('group_name', Integer, ForeignKey('group.group_name'))
)

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    # Basic integer primary key
    username = Column(VARCHAR(30), primary_key=True, info={"verbose_name": "Username"})
    first_name = Column(String(30), info={"verbose_name": "First Name"})
    last_name = Column(String(30), info={"verbose_name": "Last Name"})
    institution = Column(String(30), info={"verbose_name": "Institution"})
    roles = relationship("Role", secondary=role_association_table, back_populates="users")
    groups = relationship("Group", secondary=group_association_table, back_populates="users")

class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}
    role_name = Column(
        String(30),
        primary_key=True,
        info={
            "verbose_name": "Role",
            "choices": ["Admin", "Write", "Read"],
            "required": True,
        },
    )
    users = relationship("User", secondary=role_association_table, back_populates="roles")
    role_description = Column(String(30), info={"verbose_name": "Role Description"})

class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'extend_existing': True}
    group_name = Column(String(30),primary_key=True,info={"verbose_name": "Group Name"})
    users = relationship("User", secondary=group_association_table, back_populates="groups")
