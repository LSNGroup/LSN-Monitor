# -*- coding: utf-8 -*-
import logging
from flask import g
from sqlalchemy import and_
from lsn_monitor_end.db.lsn_db.User import User

class UserService():
    """
    登陆服务
    """
    @staticmethod
    def login_check(username, password):
        """
        验证用户密码是否正确
        :return:
        """
        try:
            print 1
            user = g.mysql_db.query(User).filter(and_(User.username == username,User.password == password)).first()
            if user is None:
                return False
            else:
                return True
        except Exception, e:
            logging.error("login_check fail : {0}\n".format(e))
            return False