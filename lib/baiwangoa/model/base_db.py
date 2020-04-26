#
# coding=utf-8

import logging
from .operate_db import OperationDB
from .models import ApplyInfo, AssetsDict, AssetsInfo, EmployeeInfo

logger = logging.getLogger(__name__)


class BaseDB(object):
    """创建于数据层交互的指定接口, 继承后使用"""

    db = OperationDB()  # DML db

    def __init__(self):
        pass

    def _set_attr(self, obj, **kwargs):
        """ set object attr, can be a Base

        :param obj: object
        :param kwargs: obj need attrs
        :return:
        """
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

    def response(self):
        """抽象出来的方法，继承BaseDB方法的需要override"""
        raise NotImplementedError

    def run(self):
        """可以用于后序对response前后进行操作"""
        return self.response()

