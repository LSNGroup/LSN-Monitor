# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer
from lsn_monitor_end.db import Base


class StatusRecordTbl(Base):

    __tablename__ = 'status_record_tbl'

    id = Column(Integer, primary_key=True)
    record_time = Column(Integer, unique=False)
    online_tree_num = Column(Integer, unique=False)
    online_branch_num = Column(Integer, unique=False)
    online_leaf_num = Column(Integer, unique=False)
    total_online_device_num = Column(Integer, unique=False)
    total_streaming_device_num = Column(Integer, unique=False)
    total_push_channels = Column(Integer, unique=False)
    total_connection_lines = Column(Integer, unique=False)

    def __init__(self, record_time, online_tree_num, online_branch_num, online_leaf_num, total_online_device_num,
                 total_streaming_device_num, total_push_channels, total_connection_lines):
        self.record_time = record_time
        self.online_tree_num = online_tree_num
        self.online_branch_num = online_branch_num
        self.online_leaf_num = online_leaf_num
        self.total_online_device_num = total_online_device_num
        self.total_streaming_device_num = total_streaming_device_num
        self.total_push_channels = total_push_channels
        self.total_connection_lines = total_connection_lines

    def __repr__(self):
        return '<StatusRecordTbl %r>' % self.record_time