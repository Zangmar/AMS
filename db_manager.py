#
# coding=utf-8

"""
Test

The module main use to deal wiht Creat and Drop DB
"""

import logging
from flask_script import Manager
from lib.baiwangoa.model import db
"""These models must be added"""
from lib.baiwangoa.model.models import *

logger = logging.getLogger()

db_manager = Manager()


@db_manager.command
def db_init():
    db.create_all()
    try:
        # 执行插入管理员的sql
        sql_admin = "insert into employee_info (phone, password, permission, name)\
                        values ('{phone}', '{password}', {permission}, '{name}')".\
                        format(
                            phone='13466428991',
                            password='pbkdf2:sha256:50000$565JagVL$07916840ccb4e7ef615f5acc245baf2a57c2d99bc9869729740897a117da053c',
                            permission=3,
                            name='admin'
                    )
        db.session.execute(sql_admin)
        # 执行字典表的插入sql
        assets_dict_list = [{'name': '苹果高配', 'code': 'DZSB0', 'pre_type': '电子设备', 'type_': '笔记本电脑'},
                            {'name': '苹果低配', 'code': 'DZSB1', 'pre_type': '电子设备', 'type_': '笔记本电脑'},
                            {'name': '戴尔高配', 'code': 'DZSB2', 'pre_type': '电子设备', 'type_': '笔记本电脑'},
                            {'name': '戴尔低配', 'code': 'DZSB3', 'pre_type': '电子设备', 'type_': '笔记本电脑'}
                    ]
        for assets_dict in assets_dict_list:
            sql_assets_dict = "insert into assets_dict (name, code, pre_type, type_)\
                                values ('{name}', '{code}', '{pre_type}', '{type_}')".\
                                format(
                                    name=assets_dict['name'], code=assets_dict['code'],
                                    pre_type=assets_dict['pre_type'], type_=assets_dict['type_']
                                )
            db.session.execute(sql_assets_dict)
        # commit 
        db.session.commit()
        logger.info('DB init success!')
    except Exception as e:
        logger.error("DB init error: {}".format(e))


@db_manager.command
def db_drop():
    choice = int(raw_input('are sure to drop db?\n1.no\n2.yes\n'))
    if choice == 2:
        db.drop_all()
        logger.info('DB drop success!')
    else:
        logger.info('DB bye')

