# -*- coding: utf-8 -*-
import logging
from flask import g
from sqlalchemy import and_, func
# from lsn_monitor_end.db.lsn_db.StreamRecordTbl import StreamRecordTbl
from lsn_monitor_end.db.lsn_db.StatusRecordTbl import StatusRecordTbl
from datetime import date, timedelta
import time, datetime

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
            start_time = conditions.get("start_time")
            end_time = conditions.get("end_time")
            total_online_device_num = g.mysql_db.query(StatusRecordTbl.total_online_device_num).\
                filter(and_(StatusRecordTbl.record_time >= start_time,StatusRecordTbl.record_time < end_time)).first()
            # data["total_online_device_num"] = total_online_device_num
            return total_online_device_num[0] if total_online_device_num else 0
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
            today = time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d"))- 28800
            yesterday = today - 86400
            node_num_yesterday = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(and_(StatusRecordTbl.record_time >= yesterday, StatusRecordTbl.record_time < today)).\
                order_by("record_time desc").first()
            node_num_today = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(StatusRecordTbl.record_time >= today).order_by("record_time desc").first()
            node_num_y = node_num_yesterday[0] if node_num_yesterday else 0
            node_num_t = node_num_today[0] if node_num_today else 0
            node_new = node_num_t - node_num_y
            return node_new
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False

    @staticmethod
    def maximum_forwarding_series(conditions= []):
        """
        最大转发级数
        :return:
        """
        try:
            today = time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), "%Y-%m-%d"))
            # yesterday = today + timedelta(days=-1)
            # # node_num_yesterday = g.mysql_db.query(StatusRecordTbl.online_star_num). \
            # #     filter(and_(StatusRecordTbl.record_time >= yesterday, StatusRecordTbl.record_time < today)). \
            # #     order_by("record_time desc").first()
            maximum_forwarding_series = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(StatusRecordTbl.record_time >= today).order_by("record_time desc").first()
            # data["maximum_forwarding_series"] = maximum_forwarding_series
            return maximum_forwarding_series[0] if maximum_forwarding_series else 0
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False

    @staticmethod
    def connection_count(conditions= []):
        """
        查询线路连接数
        :return:
        """
        try:
            data = dict()
            start_time = conditions.get("start_time")
            end_time = conditions.get("end_time")
            connection_count_num = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(and_(StatusRecordTbl.record_time >= start_time, StatusRecordTbl.record_time < end_time)).\
                order_by("record_time desc").first()
            connection_count_avg = g.mysql_db.query(func.avg(StatusRecordTbl.total_online_device_num)). \
                filter(and_(StatusRecordTbl.record_time >= start_time, StatusRecordTbl.record_time < end_time))
            connection_count_max = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(and_(StatusRecordTbl.record_time >= start_time, StatusRecordTbl.record_time < end_time)). \
                order_by("total_online_device_num desc").first()
            connection_count_min = g.mysql_db.query(StatusRecordTbl.total_online_device_num). \
                filter(and_(StatusRecordTbl.record_time >= start_time, StatusRecordTbl.record_time < end_time)). \
                order_by("total_online_device_num asc").first()
            data["connection_count_num"] = connection_count_num
            data["connection_count_avg"] = connection_count_avg
            data["connection_count_max"] = connection_count_max
            data["connection_count_min"] = connection_count_min
            return connection_count_num[0] if connection_count_num else 0
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False

    @staticmethod
    def switched_wait_delay(conditions= []):
        """
        查询新增节点数
        :return:
        """
        try:
            # today = datetime.strptime(str(date.today(), '%Y-%m-%d'))
            # yesterday = today + timedelta(days=-1)
            # node_num_yesterday = g.mysql_db.query(StatusRecordTbl). \
            #     filter(and_(StatusRecordTbl.record_time >= yesterday, StatusRecordTbl.record_time < today)). \
            #     order_by("record_time desc").first()
            # node_num_today = g.mysql_db.query(StatusRecordTbl). \
            #     filter(StatusRecordTbl.record_time >= today).order_by("record_time desc").first()
            switched_wait_delay = 200
            return switched_wait_delay
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False