# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from lsn_monitor_end.db import Base
# from datetime import datetime
# from sqlalchemy.dialects.postgresql import JSON


class StreamRecordTbl(Base):

    __tablename__ = 'stream_record_tbl'

    id = Column(Integer, primary_key=True)
    sender_node_id = Column(String(20), unique=False)
    record_time = Column(Integer, unique=False)
    source_node_id = Column(String(20), unique=False)
    object_device_node_id = Column(String(20), unique=False)
    object_guaji_node_id = Column(String(20), unique=False)
    begin_time = Column(Integer, unique=False)
    end_time = Column(String(11), unique=False)
    stream_flow = Column(Integer, unique=False)

    def __init__(self, record_time, sender_node_id, source_node_id, object_device_node_id,
                 object_guaji_node_id, begin_time, end_time, stream_flow):
        self.record_time = record_time
        self.sender_node_id = sender_node_id
        self.source_node_id = source_node_id
        self.object_device_node_id = object_device_node_id
        self.object_guaji_node_id = object_guaji_node_id
        self.begin_time = begin_time
        self.end_time = end_time
        self.stream_flow = stream_flow

    def __repr__(self):
        return '<StreamRecordTbl %r>' % self.sender_node_id