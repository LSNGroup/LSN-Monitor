# _*_ coding: utf-8 _*_
from flask import ( Blueprint, session, jsonify, request)
from lsn_monitor_end.admin.main import LoginMain
admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录逻辑
    post： 登录操作
    get:   验证用户是否登录
    :return:
    """
    data = dict()
    csrf_token = LoginMain.token_uuid()
    session['csrf_token'] = csrf_token
    try:
        # import ast
        # data =  ast.literal_eval(request.data) if request.method == 'POST' else  request.args
        if request.method == 'POST':
            data = request.form.to_dict()
            username = data.get('username', '')
            password = data.get('password', '')
            #验证用户名，密码是否正确，并做相关业务处理
            check_password_info = LoginMain.login_check(username, password)
            #验证成功返回1 失败返回0
            return jsonify({'code': 200, 'status': check_password_info['status'],
                            'data': check_password_info.get('status'), 'message': check_password_info['message'],
                            'token': ''})
    except Exception, e:
        return jsonify({'code': 500, 'status': 0, 'data': data, 'message': '1111111111', 'token': ''})
    return jsonify({'code': 200, 'status': 1, 'data': data, 'message': '登录成功', 'token': csrf_token})


@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    退出登录，清空session
    :return:
    """
    session.clear()
    return jsonify({'code': 200, 'status': 1, 'data': [], 'message': 'logout success', 'token': ''})
