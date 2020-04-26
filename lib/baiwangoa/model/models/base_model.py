#
# coding=utf-8


from datetime import datetime
from lib.baiwangoa.model import db


class BaseMix(object):
    """"That is a base model of other models"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="主键")
    create_time = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    change_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment="更改时间")
    specifications = db.Column(db.String(200), nullable=True, default='', comment="备注")  # 默认空字符串
