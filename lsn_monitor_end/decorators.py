# -*- coding: utf-8 -*-
"""Define decorators for views."""
import logging
from functools import wraps
from datetime import datetime
import uuid
import threading
import sys
from copy import deepcopy
import cProfile
import pstats
from sqlalchemy.exc import SQLAlchemyError
from flask import g, session, request, jsonify, current_app, render_template
import simplejson as json
import re
from multiprocessing.pool import ThreadPool
import hashlib
import pickle


class with_db_retry(object):
    """Decorator for view functions to make it reconnect database automatically."""
    def __init__(self, retries=3):
        self._retries = 3

    def __call__(self, func):
        @wraps(func)
        def func_with_db_reconnect(*args, **kwargs):
            retries = self._retries
            while True:
                try:
                    return func(*args, **kwargs)
                except SQLAlchemyError:
                    retries -= 1
                    if retries == 0:
                        raise
        return func_with_db_reconnect


def login_required(f):
    """
    校验用户是否登录
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('csrf_token', '')
        username = session.get('username', None)
        if username:
            return f(*args, **kwargs)
        else:
            return jsonify({'code': 303, 'status': 0, 'message': u'请登录系统', 'data': [], 'token': token})
    return decorated_function


def permission_required(app_ids):
    """
    登录用户权限校验
    :param app_id:
    :return:
    """
    def decorated_function(f):
        @wraps(f)
        def __decorated_function(*args, **kwargs):
            token = session.get('csrf_token', '')
            username = session.get('username', None)
            uid = session.get('uid', None)
            if app_ids is None:
                return jsonify({'code': 403, 'status': 0, 'message': u'当前用户没有该APP权限',
                                'data': [], 'token': token})
            app_ids_list = app_ids.split(',')
            if username and uid:
                result_info = LoginManage.get_login_user_app_menus(uid)
                if result_info['status'] == 1:
                    if set(app_ids_list) & set(result_info["data"]):
                        return f(*args, **kwargs)
                    else:
                        return jsonify({'code': '302', 'status': 0, 'data': [],
                                        'message': u'当前用户没有该APP权限', 'token': token})
                else:
                    return jsonify({'code': '500', 'status': 0, 'data': [],
                                    'message': u'服务器异常', 'token': token})
            else:
                return jsonify({'code': 303, 'status': 0, 'data': [],
                                'message': u'登录超时，请重新登录', 'token': token})
        return __decorated_function
    return decorated_function


def admin_required(f):
    '''check user whether or not logined'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''check user whether or not id admin'''
        token = session.get('csrf_token', '')
        username = session.get('username', None)
        uid = session.get('uid', None)
        first_login = session.get('first_login', None)
        updating_sid = current_app.cache.get(UPDATE_CACHE_KEY)
        if first_login:
            return jsonify({'status': 400, 'message': u'第一次登录必须修改登录密码', 'token': token})
        if updating_sid and updating_sid != session.get('sid'):
            session.clear()
            return jsonify({'status': 302, 'message': u'系统正在升级，请稍后重新登录', 'token': token})
        if username and uid:
            if uid == 1:
                return f(*args, **kwargs)
            return jsonify({'status': 302, 'message': u'没有权限', 'token': token})
        else:
            return jsonify({'status': 302, 'message': u'登录超时，请重新登录', 'token': token})

    return decorated_function


def exception_catch(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('csrf_token', '')
        try:
            return f(*args, **kwargs)
        except ShowError, e:
            return jsonify({'status': 500, 'message': e.message, 'token': token})
        except Exception, e:
            logging.error('catch exception: %s, function name : %s ' % (str(e), f.__name__), exc_info=1)
            return jsonify({'status': 500, 'message': u'服务器内部错误', 'token': token})
    return decorated_function


def app_required(appname):
    def decorated_function(f):
        @wraps(f)
        def __decorated_function(*args, **kwargs):
            token = session.get('csrf_token', '')
            username = session.get('username', None)
            uid = session.get('uid', None)
            first_login = session.get('first_login', None)
            updating_sid = current_app.cache.get(UPDATE_CACHE_KEY)
            if first_login:
                return jsonify({'status': 400, 'message': u'第一次登录必须修改登录密码', 'token': token})
            if updating_sid and updating_sid != session.get('sid'):
                session.clear()
                return jsonify({'status': 302, 'message': u'系统正在升级，请稍后重新登录', 'token': token})
            if username and uid:
                apps = UserManage.get_valid_privilege_by_uid(uid)['app_menu']["apps"]
                appname_list = [app['name'] for app in apps]
                if appname in appname_list:
                    return f(*args, **kwargs)
                return jsonify({'status': 302, 'message': u'对 %s 模块没有权限' % appname, 'token': token})
            else:
                return jsonify({'status': 302, 'message': u'登录超时，请重新登录', 'token': token})
        return __decorated_function
    return decorated_function


def with_es_retry(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('csrf_token', '')
        if not g.es:
            g.es = EsBase.create_es_client()
        if g.es:
            return f(*args, **kwargs)
        logging.error('es not initialize')
        return jsonify({'status': 500, 'message': u'ES未初始化配置', 'token': token})
    return decorated_function


def update_session(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        session.modified = True
        return func(*args, **kwargs)
    return decorated_function


def token_uuid():
    uid = ''
    uname = ''
    uid = str(uuid.uuid1())
    uname = session.get('username', '')
    return hashlib.md5(uid+uname).hexdigest()


def csrf_protect(f, template=None):
    """
    处理频繁请求操作或跨站请求
    :param f:
    :param template: 4.3模板路径
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "POST":
            token = session.pop('csrf_token', '')
            stime = session.get('csrf_timeout', '1900-01-01 00:00:00')
            now = datetime.now()
            if not stime or (not is_time_str(stime)):
                if template:
                    return render_template(template, data={'status': 403})
                # return jsonify({'status': 403, 'message': u'操作失败,请刷新页面后重新尝试！'})
                return jsonify({'code': 200, 'status': 0, 'message': u'请勿重复提交,刷新页面后重新尝试！', "token": token})
            start = datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
            if now > start:
                delta = now - start
            else:
                delta = start - now
            # _token = request.form.get('csrf_token') or request.get_json(force=True).get('_csrfToken') or request\
            #     .get_json(force=True).get('csrf_token')
            # if delta.seconds > 3600 or (not token) or token != _token:
            if delta.seconds > 3600:
                if template:
                    return render_template(template, data={'status': 403})
                # return jsonify({'status': 403, 'message': u'操作失败,请刷新页面后重新尝试！'})
                return jsonify({'code': 200, 'status': 0, 'message': u'请勿重复提交,刷新页面后重新尝试！', "token": token})
        return f(*args, **kwargs)
    return decorated_function


def generate_csrf_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'csrf_token' not in session:
            session['csrf_token'] = token_uuid()
        session['csrf_timeout'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f(*args, **kwargs)
    return decorated_function


class md5_filter(object):

    LOCAL_KEY = "TianYanNgsoc123"

    def __init__(self, flag=0, local_key='', filter_params=()):
        self.filter_params = filter_params
        self.local_key = local_key if flag == 0 and local_key else md5_filter.LOCAL_KEY
        self.session_flag = flag

    def get_request_md5(self):
        form = request.json if request.json else request.form if request.method == "POST" else request.args
        url = str(request.base_url)
        route = str(url).split("ngsoc")[1]
        remote_md5 = str(form.get("md5", ""))
        if self.session_flag:
            md5_key = str(route)
        else:
            md5_key = self.local_key
        for key in self.filter_params:
            md5_key += str(form.get(key, ""))
        md5 = hashlib.md5()
        md5.update(md5_key)
        local_md5 = str(md5.hexdigest())
        return True if local_md5 == remote_md5 else False

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                if self.get_request_md5():
                    return func(*args, **kwargs)
                return jsonify({'status': 403, 'message': u'Md5不合法', 'data': ''})
            except Exception, e:
                logging.warning("md5 compare failed " + str(e))
                return jsonify({'status': 403, 'message': u'Md5不合法', 'data': ''})
        return decorated_function


# add for pager info transfer
local_page_info = threading.local()


def page_param(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        form = request.form if request.method == "POST" else request.args
        param = {'page': form.get('page', '1'), 'limit': form.get('limit', '1'), 'orderBy': form.get('orderBy', 'id')}
        list_all_condition = form.get('list_all', None)
        if list_all_condition is not None:
            param['limit'] = sys.maxint
        local_page_info.param = param
        return f(*args, **kwargs)
    return decorated_function


def check_special(str_check):
    """
    转移特殊字符
    :param str_check:
    :return:
    """
    if str_check:
        pattern = re.compile(r'\*+|\?+|%+')
        repeat = list(set(pattern.findall(str_check)))
        while repeat:
            k = repeat.pop()
            str_check = str_check.replace(k, "\\" + k)
    return str_check


def query_params(*es_query_params):
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """
    def _wrapper(func):
        @wraps(func)
        def _wrapped(kwargs):

            params = deepcopy(kwargs) if kwargs else {}

            for p in es_query_params:
                if p in kwargs:
                    params[p] = check_special(kwargs.get(p))

            # don't treat ignore and request_timeout as other params to avoid escaping

            return func(params)
        return _wrapped
    return _wrapper


def judge_param_legal(params):
    illegal_charset = r'.*[\s?%\*]+'
    pattern = re.compile(illegal_charset)
    if isinstance(params, list):
        for param in params:
            match = pattern.match(str(param).strip())
            if match:
                return True
        return False
    else:
        match = pattern.match(str(params).strip())
        return True if match else False


def illegal_param_check(*check_param):
    def _wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = session.get('csrf_token', '')
            form = request.form if request.method == "POST" else request.args
            all_params = form if form else request.json
            if not all_params:
                return f(*args, **kwargs)
            else:
                check_keys = check_param if check_param else all_params.keys()
                for key in check_keys:
                    if key[-2:] == '[]':
                        to_check = all_params.getlist(key)
                    else:
                        to_check = all_params.get(key)
                    if judge_param_legal(to_check):
                        return jsonify(status=200, message='illegal param:' + str(key), 
                                       data={"status": 201}, token=token)
                return f(*args, **kwargs)
        return decorated_function
    return _wrapper


def filter_privilege(f):
    """
    check data filter_privilege, including industry, province and city
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        params = request.form if request.method == "POST" else request.args if request.args else \
            request.json if request.json else {}
        token = session.get('csrf_token', '')
        region = session["region"]
        industry_list = session["industry"]
        industry_status, region_status = get_params_status(params)
        msg1 = u'此行业不在权限范围内,请确认后传参数！'
        msg2 = u'此区域不在权限范围内,请确认后传参数！'
        if industry_status and region_status:
            r_status = get_region_status(params, region)
            i_status = get_industry_status(params, industry_list)
            if r_status and i_status:
                return f(*args, **kwargs)
            elif r_status:
                return jsonify({'status': 403, 'message': msg1, "token": token})
            elif i_status:
                return jsonify({'status': 403, 'message': msg2, "token": token})
            return jsonify({'status': 403, 'message': u'行业和区域权限不足！', "token": token})
        elif industry_status:
            i_status = get_industry_status(params, industry_list)
            if i_status:
                return f(*args, **kwargs)
            return jsonify({'status': 403, 'message': msg1, "token": token})
        elif region_status:
            r_status = get_region_status(params, region)
            if r_status:
                return f(*args, **kwargs)
            return jsonify({'status': 403, 'message': msg2, "token": token})
        else:
            logging.warning("使用默认的区域和行业权限！")
            return f(*args, **kwargs)
    return decorated_function


class use_cache(object):
    """Decorator for view functions to make it reconnect database automatically."""
    IGNORE_PARAM_KEYWORD = {"r", 'csrf_token'}

    REDIS_CACHE = Cache(**ROUTE_CACHE)

    def __init__(self, available_time=5, ignore_params=()):
        self._available_time = available_time
        self._exclude_params = ignore_params

    def get_request_md5(self):
        url = str(request.base_url)
        form = request.form if request.method == "POST" else request.args
        params = form if form else request.json if request.json else {}
        params_copy = params.copy()
        for key in use_cache.IGNORE_PARAM_KEYWORD:
            if key in params_copy:
                params_copy.pop(key)

        for key in self._exclude_params:
            if key in params_copy:
                params_copy.pop(key)

        params_list = params_copy.items()
        params_list.sort(key=lambda x: x[0])
        url += '?'
        for item in params_list:
            url += '='.join([str(x) for x in item])
            url += "&"

        url += json.dumps(session.get("industry", {}))
        url += json.dumps(session.get("data_region", {}))
        md5 = hashlib.md5()
        md5.update(url)
        return str(md5.hexdigest())

    def set_result_to_data(self, key_md5, data):
        use_cache.REDIS_CACHE.set(key_md5, data, format="str", ex=self._available_time)

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                request_md5 = self.get_request_md5()
                result = use_cache.REDIS_CACHE.get(request_md5, format="str")
                # > 0 for success
                if result is not None:
                    res = json.loads(result)
                    res["token"] = session.get('csrf_token', '')
                    # logging.warn("cache is scored....")
                    return jsonify(**res)
                # 0 for some other same request is execute, try to waiting  unless the other same route returned
                else:
                    # logging.warn("cache is out date or the first execute...")
                    response = func(*args, **kwargs)
                    self.set_result_to_data(request_md5, response.get_data())
                    return response
            except Exception, e:
                logging.warn("cache exception for " + str(e) + ", function will directly execute")
                return func(*args, **kwargs)
        return decorated_function


class func_cache(object):

    REDIS_CACHE = Cache(**ROUTE_CACHE)

    def __init__(self, available_time=20, permit_filter=None, gen_key_func=None, prefix=''):
        self._available_time = available_time
        self._permit_filter = permit_filter if permit_filter else func_cache.default_permit_filter
        self._gen_key_func = gen_key_func
        self._prefix = prefix

    @staticmethod
    def default_permit_filter(*args, **kwargs):
        return True

    @staticmethod
    def get_md5_key(func_name, args, kwargs):
        """
        :param func_name:
        :return:
        """
        str_key = str(func_name) + json.dumps(args) + json.dumps(kwargs)
        md5 = hashlib.md5()
        md5.update(str_key)
        return str(md5.hexdigest())

    @staticmethod
    def erase_cache(*key_prefix):
        try:
            for key in key_prefix:
                key_list = func_cache.REDIS_CACHE.keys(str(key) + "*")
                func_cache.REDIS_CACHE.delete(*key_list) if key_list else None
        except Exception, e:
            logging.warning("erase cache:" + str(key_prefix) + " :" + e.message)

    def set_result_to_data(self, key_md5, data):
        func_cache.REDIS_CACHE.set(key_md5, {"data": pickle.dumps(data)}, format="json", ex=self._available_time)

    def __call__(self, func):
        """
        :param func:
        :type func: func
        :return:
        """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            """
            :param param:
            :type param: dict
            :return:
            """
            try:
                func_name = str(func.__module__) + "." + str(func.__name__)
                if self._permit_filter(*args, **kwargs) is False:
                    return func(*args, **kwargs)
                md5_key = self._gen_key_func(*args, **kwargs) if self._gen_key_func else \
                    func_cache.get_md5_key(func_name, args, kwargs)
                md5_key = self._prefix + md5_key
                result = func_cache.REDIS_CACHE.get_json(md5_key)
                if result is not None:
                    logging.debug(func_name + " scored...")
                    return pickle.loads(result.get("data"))
                else:
                    res = func(*args, **kwargs)
                    self.set_result_to_data(md5_key, res)
                    return res
            except Exception, e:
                logging.warn("exception occur in func_cache: " + str(func.__name__) + str(e))
                return func(*args, **kwargs)
        return decorated_function


def erase_cache(*key_prefix):
    """
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            func_cache.erase_cache(*key_prefix)
            return func(*args, **kwargs)
        return profiled_func
    return wrapper


class audit_response_t(object):

    PATTERN = re.compile("[$][{][^{}]+[}]")
    AUDIT_THREAD_POOL = ThreadPool(processes=2)

    def __init__(self, **kwargs):
        self.params = kwargs

    @staticmethod
    def analyse_params(response, **params):
        new_params = dict()
        for key, value in params.items():
            if isinstance(value, (str, unicode)):
                match_list = audit_response_t.PATTERN.findall(value)
                if isinstance(match_list, list):
                    for patch in match_list:
                        exe_result = eval(patch[2: -1])
                        value = str(value).replace(patch, str(exe_result))
            new_params[key] = value
        return new_params

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            response = func(*args, **kwargs)
            try:
                new_params = audit_response_t.analyse_params(json.loads(response.get_data()), **self.params)
                audit_response_t.add_audit(**new_params)
            except Exception, e:
                logging.warn("add_audit_t in decorator except for " + str(e))
            return response
        return decorated_function


def do_cprofile(filename):
    """
    性能分析装饰器定义
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            do_prof = 1
            if do_prof:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                ps = pstats.Stats(profile)
                ps.dump_stats(filename)
                # ps.print_stats()
            else:
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper


class AddSysLog(object):

    def __init__(self, **kwargs):
        self.params = kwargs

    def __call__(self, func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            response = func(*args, **kwargs)
            new_params = self.params
            # token = session.get('csrf_token', '')
            uid = session.get('uid', None)
            response_data = json.loads(response.data)
            if response_data['status'] == 1:
                result = u'成功'
            else:
                result = u'失败'
            new_params['result'] = result
            try:
                # user_id = g.pg_db.query(User.id).filter(User.username == username).scalar()
                new_params['user_id'] = uid
                SystemCommonLog.add_log(new_params)
            except Exception, e:
                logging.error("func:add system common log failed {0}\n".format(e))
            return response
        return decorated_function


if __name__ == "__main__":
    pass
