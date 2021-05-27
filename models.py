from datetime import timedelta
from flask import Flask, render_template, request, jsonify ,session as ss ,json
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

Base = declarative_base()
video_user = Table('video_user', Base.metadata,
                     Column('user_id', Integer, ForeignKey('users.id')),
                     Column('vidoe_id', Integer, ForeignKey('video.video_id'))
                     )

class User(Base):
    __tablename__ = "users"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String)
    surname = Column('surname', String)
    username = Column('username', String)
    email = Column('email', String)
    password = Column('password', String)
    role = Column('role', String)



    def __init__(self, name=None, username=None, surname=None, email=None, password=None, role="user"):
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.email = email
        self.role = role


class Video(Base):
    __tablename__ = "video"

    video_id = Column('video_id', Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', String)
    time = Column('time', String)


    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'time': self.time
        }