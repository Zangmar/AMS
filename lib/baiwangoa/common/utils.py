#
# coding=utf-8

"""辅助模块"""

import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


def to_dict(obj):
    """将 ImmutableMultiDict 转换为 Dict"""
    dct = {}
    for k, v in obj.items():
        dct[k] = v
    return dct


def excel_parser(path):
    """将excel解析为相应数据结构

    :return: [list{dict}]
    """
    import xlrd  # used by excel_parser
    ans_list = []  # ret list
    # 1 open file
    u_path = path.decode('utf8')  # 转为unicode
    try:
        workbook = xlrd.open_workbook(u"{u_path}".format(u_path=u_path))
        sheet_names = workbook.sheet_names()
        # 2 parser first page
        sheet_one = workbook.sheet_by_name(sheet_names[0])  # 只对第一页基进行解析
    except IOError as e:
        # logger.error('This excel not exist!')
        raise ValueError('{}: This excel not exist!'.format(u_path))
    # 3 遍历当前页的数据
    sheet_keys = sheet_one.row_values(0)  # key_list
    row_length = sheet_one.nrows  # len row
    col_length = sheet_one.ncols  # len col
    for row_num in xrange(1, row_length):
        row_dict = {}
        row = sheet_one.row_values(row_num)  # List
        for col_num in xrange(col_length):
            row_dict[sheet_keys[col_num]] = row[col_num]  # if row[col_num] ret, else None
        ans_list.append(row_dict)
    return ans_list


def to_date(date_string):
    """"将date的string转换为datetime.date
    
    2019-01-03 --> datetime.date
    return datetime.date
    """
    import datetime
    date_list = date_string.split('-')
    return datetime.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    # from datetime import datetime
    # from xlrd import xldate_as_tuple
    # date_list = datetime(*xldate_as_tuple(date_string, 0)).strftime("%Y-%m-%d")
    # return date_list

def timer(func):
    """计算函数执行时间"""
    @wraps(func)
    def inner(*args, **kwargs):
        t1 = time.time()
        ret = func(*args, **kwargs)
        t2 = time.time()
        print '{} Time Cost: {} s'.format(func.__name__, t2-t1)
        return ret
    return inner


