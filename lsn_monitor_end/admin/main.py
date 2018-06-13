# -*- coding: utf-8 -*-
import logging
import uuid
import hashlib
from flask import g, session
from lsn_monitor_end.db.lsn_db.User import User
from lsn_monitor_end.admin.service import UserService


class LoginMain(object):
    '''登陆相关'''

    @staticmethod
    def token_uuid():
        user_id = str(uuid.uuid1())
        user_name = session.get('username', '')
        return hashlib.md5(user_id + user_name).hexdigest()

    @staticmethod
    def login_check(username, password):
        """
        验证用户名，密码是否正确
        :param username:
        :param password:
        :return:
        """
        try:
            user_info = g.mysql_db.query(User).filter(User.username == username).first()
            if not user_info:
                result_info = {'status': 0, 'message':  u'该用户不存在'}
                return result_info
            result = UserService.login_check(username, password)
            if not result:
                result_info = {'status': 0, 'message':  u'密码不正确'}
                return result_info
            else:
                result_info = {'status': 1, 'message':  u'登陆成功'}
                return result_info
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            result_info = {'status': 0, 'message':  u'未知错误'}
            return result_info


