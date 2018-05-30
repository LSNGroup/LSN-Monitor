# -*- coding: utf-8 -*-
import logging
from flask import g
from sqlalchemy import and_
from lsn_monitor_end.db.lsn_db.StreamRecordTbl import StreamRecordTbl
from lsn_monitor_end.db.lsn_db.StatusRecordTbl import StatusRecordTbl
from datetime import datetime, date, timedelta

class MonitorService():
    """
    监测
    """
    @staticmethod
    def node_online(conditions= []):
        """
        查询在线总节点数
        :return:
        """
        try:
            data = dict()
            start_time = conditions.get("start_time")
            end_time = conditions.get("end_time")
            total_online_device_num = g.mysql_db.query(StatusRecordTbl).\
                filter(and_(StatusRecordTbl.record_time >= start_time,StatusRecordTbl.record_time < end_time)).first()
            data["total_online_device_num"] = total_online_device_num
            return data
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False

    @staticmethod
    def node_new():
        """
        查询新增节点数
        :return:
        """
        try:
            data = dict()
            today = datetime.strptime(str(date.today(),'%Y-%m-%d'))
            yesterday = today + timedelta(days=-1)
            node_num_yesterday = g.mysql_db.query(StatusRecordTbl). \
                filter(and_(StatusRecordTbl.record_time >= yesterday, StatusRecordTbl.record_time < today)).\
                order_by("record_time desc").first()
            node_num_today = g.mysql_db.query(StatusRecordTbl). \
                filter(StatusRecordTbl.record_time >= today).order_by("record_time desc").first()
            data["node_new"] = node_num_today - node_num_yesterday
            return data
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False