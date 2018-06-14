# -*- coding: utf-8 -*-
import logging
from flask import g
import datetime
from lsn_monitor_end.monitor.service import MonitorService


class MonitorMain(object):
    '''监测数据相关'''

    @staticmethod
    def node_online(condition= []):
        """
        在线节点数 当前在线节点数，以及可查询历史某天在线节点数高低峰值及均值
        """
        try:
            data = MonitorService.node_online(condition)
            return data
        except Exception, e:
            logging.error("get node_online fail : {0}\n".format(e))
            result_info = {'status': 0, 'message':  u'未知错误'}
        return result_info

    @staticmethod
    def node_new():
        """
        新增节点数  以天为单位统计，全新加入的节点数
        """
        try:
            data = MonitorService.node_new()
            return data
        except Exception, e:
            logging.error("get node_new fail : {0}\n".format(e))
            result_info = {'status': 0, 'message': u'未知错误'}
        return result_info

    @staticmethod
    def connection_count(condition = []):
        """
        线路连接数 当前线路连接数，以及可查询历史某天在线节点数高低峰值及均值
        """
        try:
            data = MonitorService.connection_count(condition)
            return data
        except Exception, e:
            logging.error("get node_online fail : {0}\n".format(e))
            result_info = {'status': 0, 'message': u'未知错误'}
        return result_info

    @staticmethod
    def maximum_forwarding_series(condition= []):
        """
        最大转发级数 默认为 4 级，使用极限放大器。后续可调整为3级或2级。
        """
        try:
            data = MonitorService.maximum_forwarding_series(condition)
            return data
        except Exception, e:
            logging.error("get node_online fail : {0}\n".format(e))
            result_info = {'status': 0, 'message': u'未知错误'}
        return result_info

    @staticmethod
    def switched_wait_delay(condition= []):
        """
        切换等待时延 节点300ms无响应，则应切换线路。后续可调整为 200ms。
        """
        try:
            data = MonitorService.switched_wait_delay(condition)
            return data
        except Exception, e:
            logging.error("get node_online fail : {0}\n".format(e))
            result_info = {'status': 0, 'message': u'未知错误'}
        return result_info


