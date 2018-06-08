# _*_ coding: utf-8 _*_
from flask import ( Blueprint, session, jsonify, request)
from lsn_monitor_end.monitor.main import MonitorMain
monitor = Blueprint('monitor', __name__)

@monitor.route('/node_online', methods=['GET', 'POST'])
def monitor_info():
    """
    监控信息
    :return:
    """
    data = dict()
    try:
        import ast
        parm =  ast.literal_eval(request.data) if request.method == 'POST' else  request.args
        condition = dict()
        condition["start_time"] = parm.get('start_time')
        condition["end_time"] = parm.get('end_time')
        data["node_online"] = MonitorMain.node_online(condition)
        data["node_new"] = MonitorMain.node_new()
    except Exception, e:
        return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '服务器异常', 'token': ''})
    return jsonify({'code': 200, 'status': 1, 'data': data, 'message': 'success', 'token': ""})

