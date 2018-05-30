# -*- coding: utf-8 -*-
"""create flask app."""

import logging

from flask import Flask, g
from lsn_monitor_end.db.db import DbClass

class WingsAppHolder(object):
    def __init__(self, app, db):
        """init before request"""
        self.app = app
        self.db = db
        self.app.before_request(self.before_request)
        self.app.teardown_request(self.teardown_request)

    def before_request(self):
        """handle before request"""
        session = self.db.make_session()
        g.mysql_db = session()

        # initialize es

    def teardown_request(self, exception):
        """handle after request"""
        # session = g.apt_db
        session = g.mysql_db
        if session:
            session.close()
        if exception is not None:
            logging.warn("[{0} {1}] an exception occurred to this request:"
                         " {2}".format("app.py", "WingsAppHolder", exception), exc_info=1)


def _bind_database(app, db):
    """bind database"""
    return WingsAppHolder(app, db)


def _init_database(app, db):
    """init database"""
    db.create_table()


def init_app(settings=None, name=None):
    """create app"""
    if settings is None:
        from lsn_monitor_end import settings
        _s = settings
    else:
        _s = settings
    if name is None:
        name = __name__
    app = Flask(name)
    app.app_context().push()
    app.config.from_object(_s)
    return app


def create_app(settings=None, name=None):
    app = init_app(settings, name)
    from monitor.views import monitor
    app.register_blueprint(monitor, url_prefix='/lsn/monitor')
    from admin.views import admin
    app.register_blueprint(admin, url_prefix='/lsn/admin')

    db = DbClass(app.config.get("SQLALCHEMY_DATABASE_URI"))
    _init_database(app, db)
    _bind_database(app, db)
    return app
