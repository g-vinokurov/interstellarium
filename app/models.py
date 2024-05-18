# -*- coding: utf-8 -*-

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

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

    name = Column(String(255), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('email'),
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
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        PrimaryKeyConstraint('id', name='designer_pk')
    )


class Engineer(Base):
    __tablename__ = 'engineers'
    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        PrimaryKeyConstraint('id', name='engineer_pk')
    )


class Technician(Base):
    __tablename__ = 'technicians'
    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        PrimaryKeyConstraint('id', name='technician_pk')
    )
