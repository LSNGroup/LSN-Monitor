# -*- coding: utf-8 -*-

from lsn_monitor_end.db import Base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, desc
from lsn_monitor_end.db.lsn_db import StatusRecordTbl, StreamRecordTbl, User

from lsn_monitor_end.settings import SQLALCHEMY_DATABASE_URI

mapped_class_dic = dict(status_record_tbl=StatusRecordTbl,
                        stream_record_tbl=StreamRecordTbl,
                        user=User,
                        )


class DbClass(object):
    def __init__(self, uri):
        self._engine = create_engine(uri, echo=False, encoding="utf-8", max_overflow=30, pool_size=10)
        self._metadata = Base.metadata

    def create_table(self):
        self._metadata.create_all(self._engine)

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        Session = scoped_session(session_factory)
        return Session


class DbClassNoPool(object):
    def __init__(self, uri):
        self._engine = create_engine(uri, echo=False, encoding="utf-8", poolclass=NullPool)
        self._metadata = Base.metadata

    def make_session(self):
        session_factory = sessionmaker(bind=self._engine)
        db_session = scoped_session(session_factory)
        return db_session


def query_db(session, table_name, filter_dic=None, order_attr=None, isdesc=False, offset=0, limit=-1):
    """return a list, each element is an object """
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        mapped_class = mapped_class_dic[table_name]
        my_obj = session.query(mapped_class)
        if filter_dic:
            # 等于条件
            if "=" in filter_dic:
                filter_dic_eq = filter_dic["="]
                for attr in filter_dic_eq:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_eq: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_eq:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) == filter_dic_eq[attr])
            # 小于条件
            if "<" in filter_dic:
                filter_dic_lt = filter_dic["<"]
                for attr in filter_dic_lt:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_lt: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_lt:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) < filter_dic_lt[attr])
            # 小于等于条件
            if "<=" in filter_dic:
                filter_dic_le = filter_dic["<="]
                for attr in filter_dic_le:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_le: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_le:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) <= filter_dic_le[attr])
            # 大于条件
            if ">" in filter_dic:
                filter_dic_gt = filter_dic[">"]
                for attr in filter_dic_gt:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_gt: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_gt:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) > filter_dic_gt[attr])
            # 大于等于条件
            if ">=" in filter_dic:
                filter_dic_ge = filter_dic[">="]
                for attr in filter_dic_ge:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_ge: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_ge:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) >= filter_dic_ge[attr])
            # in包含条件
            if "in_" in filter_dic:
                filter_dic_gt = filter_dic["in_"]
                for attr in filter_dic_gt:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_gt: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_gt:
                    my_obj = my_obj.filter(getattr(mapped_class, attr).in_(filter_dic_gt[attr]))
            # 模糊查询
            if "~" in filter_dic:
                filter_dic_like = filter_dic["~"]
                for attr in filter_dic_like:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_like: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                           table_name))
                for attr in filter_dic_like:
                    my_obj = my_obj.filter(getattr(mapped_class, attr).like("%{}%".format(filter_dic_like[attr])))

        if order_attr:
            if not hasattr(mapped_class, order_attr):
                raise Exception("order_attr: '{0}' is not an attribute of table '{1}'".format(order_attr, table_name))
            if isinstance(isdesc, bool) and isdesc:
                my_obj = my_obj.order_by(desc(getattr(mapped_class, order_attr)))
            elif isinstance(isdesc, bool) and (not isdesc):
                my_obj = my_obj.order_by(getattr(mapped_class, order_attr))
            else:
                raise Exception("isdesc: must be 'bool' type")
        if (not isinstance(offset, int)) or (not isinstance(limit, int)) or offset < 0 or limit < -1:
            raise Exception("argument is illegal")
        if limit == -1:
            my_obj = my_obj[offset:]
        else:
            my_obj = my_obj[offset:(offset + limit)]
        return my_obj
    except Exception as e:
        session.rollback()
        raise Exception(e)


def query_db_count(session, table_name, filter_dic=None):
    """ return an integer """
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        mapped_class = mapped_class_dic[table_name]
        my_obj = session.query(mapped_class)
        if filter_dic:
            # 等于条件
            if "=" in filter_dic:
                filter_dic_eq = filter_dic["="]
                for attr in filter_dic_eq:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_eq: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_eq:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) == filter_dic_eq[attr])
            # 小于条件
            if "<" in filter_dic:
                filter_dic_lt = filter_dic["<"]
                for attr in filter_dic_lt:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_lt: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_lt:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) < filter_dic_lt[attr])
            # 小于等于条件
            if "<=" in filter_dic:
                filter_dic_le = filter_dic["<="]
                for attr in filter_dic_le:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_le: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_le:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) <= filter_dic_le[attr])
            # 大于条件
            if ">" in filter_dic:
                filter_dic_gt = filter_dic[">"]
                for attr in filter_dic_gt:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_gt: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_gt:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) > filter_dic_gt[attr])
            # 大于等于条件
            if ">=" in filter_dic:
                filter_dic_ge = filter_dic[">="]
                for attr in filter_dic_ge:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_ge: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                         table_name))
                for attr in filter_dic_ge:
                    my_obj = my_obj.filter(getattr(mapped_class, attr) >= filter_dic_ge[attr])

            # 模糊查询
            if "~" in filter_dic:
                filter_dic_like = filter_dic["~"]
                for attr in filter_dic_like:
                    if not hasattr(mapped_class, attr):
                        raise Exception("filter_dic_like: '{0}' is not an attribute of table '{1}'".format(attr,
                                                                                                           table_name))
                for attr in filter_dic_like:
                    my_obj = my_obj.filter(getattr(mapped_class, attr).like("%{}%".format(filter_dic_like[attr])))

        my_obj = my_obj.count()
        return my_obj
    except Exception as e:
        session.rollback()
        raise Exception(e)


def insert_db(session, table_name, **attr_dic):
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        mapped_class = mapped_class_dic[table_name]
        for attr in attr_dic:
            if not hasattr(mapped_class, attr):
                raise Exception("attr_dic: '{0}' is not an attribute of table '{1}'".format(attr, table_name))

        mapped_table = mapped_class(**attr_dic)
        session.add(mapped_table)
        session.flush()
        insert_id = mapped_table.id
        session.commit()
        return insert_id

    except Exception as e:
        session.rollback()
        raise Exception(e)


def insert__bulk_db(session, table_name, list_objects):
    dict_list = list()
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        mapped_class = mapped_class_dic[table_name]
        for attr_dic in list_objects:
            for attr in attr_dic:
                if not hasattr(mapped_class, attr):
                    raise Exception("attr_dic: '{0}' is not an attribute of table '{1}'".format(attr, table_name))
            mapped_table = mapped_class(**attr_dic)
            dict_list.append(mapped_table)

        session.bulk_save_objects(dict_list)
        session.flush()
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        raise Exception(e)


def update_db(session, table_name, set_dic=None, filter_dic=None):
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        mapped_class = mapped_class_dic[table_name]
        if (not set_dic) or (not isinstance(set_dic, dict)):
            raise Exception("set_dic should be an instance of dict and must not be empty")
        for attr in set_dic:
            if not hasattr(mapped_class, attr):
                raise Exception("set_dic: '{0}' is not an attribute of table '{1}'".format(attr, table_name))
        ret_list = query_db(session, table_name, filter_dic)
        for obj in ret_list:
            for attr in set_dic:
                setattr(obj, attr, set_dic[attr])
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(e)
    finally:
        session.close() if session else None


def delete_db(session, table_name, filter_dic=None):
    if table_name not in mapped_class_dic:
        raise Exception("table '{0}' doesn't exist".format(table_name))
    try:
        ret_list = query_db(session, table_name, filter_dic)
        for obj in ret_list:
            session.delete(obj)
        session.flush()
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(e)


def get_db_session():
    _engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False, encoding="utf-8")
    DBSession = sessionmaker(bind=_engine)
    return DBSession