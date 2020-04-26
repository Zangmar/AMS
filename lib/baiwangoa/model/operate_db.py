#
# -*- coding:utf-8 -*-

import logging
from . import db

log = logging.getLogger(__name__)


def detect_exception(func):
    """用于对于操作db的异常处理"""

    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            error = 'Operate DB Error: {e}'.format(e=str(e))
            raise OperateDBError(error)

    return inner


class OperationDB(object):
    """ 操作DB.

    必须和表中用同一个db对象，否则增加数据后，查询会有问题：查不到数据.
    """
    def __init__(self):
        self.__db = db  # db入口，私有属性

    @detect_exception
    def add(self, obj, commit=True):
        """添加操作
        
        可以指定是否commit
        """
        self.__db.session.add(obj)
        if commit: self.__db.session.commit()

    @detect_exception
    def add_all(self, obj_tup):
        """
        :param obj_tup: List or Tuple
        :return: None
        """
        self.__db.session.add_all(obj_tup)
        self.__db.session.commit()

    @detect_exception
    def commit(self):
        """commit"""
        self.__db.session.commit()

    @detect_exception
    def delete(self, obj):
        self.__db.session.delete(obj)
        self.__db.session.commit()

    @detect_exception
    def flush(self):
        # 预提交数据
        self.__db.session.flush()


class OperateDBError(Exception):
    """Operate DB error"""
    pass
