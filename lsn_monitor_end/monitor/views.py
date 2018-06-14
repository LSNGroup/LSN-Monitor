# _*_ coding: utf-8 _*_
from flask import ( Blueprint, session, jsonify, request)
from lsn_monitor_end.monitor.main import MonitorMain
import time, datetime
monitor = Blueprint('monitor', __name__)

@monitor.route('/monitor_info', methods=['GET', 'POST'])
def monitor_info():
    """
    监控信息
    :return:
    """
    data = dict()
    try:
        # import ast
        # parm =  ast.literal_eval(request.data) if request.method == 'POST' else  request.args
        condition = dict()
        parm = request.form.to_dict()
        start_time = parm.get('startTime') \
            if parm.get('startTime')!="undefined" else datetime.datetime.now().strftime('%Y-%m-%d')
        end_time= parm.get('endTime') \
            if parm.get('endTime')!="undefined" else datetime.datetime.now().strftime('%Y-%m-%d')
        condition["start_time"] = time.mktime(time.strptime(start_time, "%Y-%m-%d")) - 28800
        condition["end_time"] = time.mktime(time.strptime(end_time, "%Y-%m-%d")) + 57599
        if condition["start_time"] > condition["end_time"]:
            return jsonify({'code': 201, 'status': 0, 'data': [], 'message': '开始时间不能大于结束时间', 'token': ''})
        data["node_online"] = MonitorMain.node_online(condition)
        data["node_new"] = MonitorMain.node_new()
        data["connection_count"] = MonitorMain.connection_count(condition)
        data["maximum_forwarding_series"] = MonitorMain.maximum_forwarding_series()
        data["switched_wait_delay"] = MonitorMain.switched_wait_delay()
        return jsonify({'code': 200, 'data': data, 'message': "查询状态成功", 'token': ''})
    except Exception, e:
        return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '服务器异常', 'token': ''})
    return jsonify({'code': 200, 'status': 1, 'data': data, 'message': 'success', 'token': ""})

