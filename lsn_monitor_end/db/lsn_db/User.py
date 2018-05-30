# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from lsn_monitor_end.db import Base


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(10), unique=True)
    password = Column(String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username