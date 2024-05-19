# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date

from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import UniqueConstraint

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(512), nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    name = Column(String(255), nullable=True)
    birthdate = Column(Date, nullable=True)
    
    department_id = Column(Integer, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('email', name='user_email_unique'),
        ForeignKeyConstraint(
            ['department_id'],
            ['departments.id'],
            ondelete='SET NULL',
            onupdate='CASCADE',
            name='user_department_department_fk'
        )
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Designer(Base):
    __tablename__ = 'designers'

    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='designer_user_fk'
        ),
        PrimaryKeyConstraint('id', name='designer_pk'),
        UniqueConstraint('user_id', name='designer_user_unique')
    )


class Engineer(Base):
    __tablename__ = 'engineers'

    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='engineer_user_fk'
        ),
        PrimaryKeyConstraint('id', name='engineer_pk'),
        UniqueConstraint('user_id', name='engineer_user_unique')
    )


class Technician(Base):
    __tablename__ = 'technicians'

    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='technician_user_fk'
        ),
        PrimaryKeyConstraint('id', name='technician_pk'),
        UniqueConstraint('user_id', name='technician_user_unique')
    )


class Laboratorian(Base):
    __tablename__ = 'laboratorians'

    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='laboratorian_user_fk'
        ),
        PrimaryKeyConstraint('id', name='laboratorian_pk'),
        UniqueConstraint('user_id', name='laboratorian_user_unique')
    )


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, autoincrement=True)
    leader_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['leader_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='department_leader_user_fk'
        ),
        PrimaryKeyConstraint('id', name='department_pk'),
        UniqueConstraint('leader_id', name='department_leader_unique')
    )
