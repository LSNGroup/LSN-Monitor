# _*_ coding: utf-8 _*_
from flask import ( Blueprint, session, jsonify, request)
from lsn_monitor_end.monitor.main import MonitorMain
monitor = Blueprint('monitor', __name__)

@monitor.route('/node_online', methods=['GET', 'POST'])
def node_online():
    """
    用户登录逻辑
    post： 登录操作
    get:   验证用户是否登录
    :return:
    """
    data = dict()
    try:
        import ast
        data =  ast.literal_eval(request.data) if request.method == 'POST' else  request.args
        condition = dict()
        condition["start_time"] = data.get('start_time')
        condition["end_time"] = data.get('end_time')
        data = MonitorMain.node_online(condition)
    except Exception, e:
        return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '服务器异常', 'token': ''})
    return jsonify({'code': 200, 'status': 1, 'data': data, 'message': 'success', 'token': ""})


@monitor.route('/node_new', methods=['GET', 'POST'])
def node_new():
    """
    用户登录逻辑
    post： 登录操作
    get:   验证用户是否登录
    :return:
    """
    data = dict()
    try:
        data = MonitorMain.node_new()
    except Exception, e:
        return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '服务器异常', 'token': ''})
    return jsonify({'code': 200, 'status': 1, 'data': data, 'message': 'success', 'token': ""})
