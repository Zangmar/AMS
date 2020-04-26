#
# coding=utf-8

"""该模块主要是用户权限相关操作"""

import logging
from functools import wraps
from flask import session, redirect, url_for, flash
from config import global_config as gconfig
from lib.baiwangoa.model.base_db import BaseDB
from lib.baiwangoa.model.models import EmployeeInfo

logger = logging.getLogger(__name__)


class LoginHP(BaseDB):
    """主要是对登录用户的身份进行分类的辅助类"""

    def __init__(self, method=None, data=None):
        self.permission_dict = gconfig.PERMISSION_DICT  # defalut三种默认权限
        self.method = method
        self.data = data if data else {}

    def validate(self):
        """登录验证"""
        phone = self.data.get('phone')
        password = self.data.get('password')
        employee = EmployeeInfo.query.filter_by(phone=phone).first()
        if employee and employee.check_password(password):  # check user and user's password
            login_user(employee)  # login user
            # return self.permission_dict[employee.permission]
            return True
        else:
            return False

    def choose_main(self):
        """选择对应的主页"""
        logger.debug(self.data)
        return self.permission_dict[self.data['permission']]
            
    def run(self):
        return getattr(self, self.method)()


def login_require(permission=0):
    """Permission Control

    主要功能: 控制视图函数的权限
    使用方法: permission: 0: all, 1: hr and admin, 2: admin, >2: non-person
    """
    def middle(func):
        @wraps(func)  # 需要将func进行包装，否则视图函数会被注册为inner
        def inner(*args, **kwargs):
            if session.get('permission') and session.get('permission') > permission:  # 该user存在，并且有权限。
                return func(*args, **kwargs)
            logging.info('have not permission')
            flash('抱歉，您没有访问它的权限')
            return redirect(url_for('auth.login'))
        return inner
    return middle


def login_user(user):
    session['user_id'] = user.id
    session['name'] = user.name
    session['permission'] = user.permission


def logout_user():
    session.clear()
