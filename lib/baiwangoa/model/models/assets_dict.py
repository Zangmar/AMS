#
# coding=utf-8

from .base_model import BaseMix
from lib.baiwangoa.model import db


class AssetsDict(db.Model, BaseMix):
    """字典表."""
    __tablename__ = 'assets_dict'
    name = db.Column(db.String(80), nullable=False, comment="资产名 ex: 联想X1, 仓库, 未受理")
    code = db.Column(db.String(40), nullable=True, comment="资产编码 ex: DZSB-171101, 722, W")
    pre_type = db.Column(db.String(80), default='', nullable=True, comment="大类 ex: 电子设备，存放位置，设备状态，申请状态")  
    type_ = db.Column(db.String(80), default='', nullable=True, comment="类型 ex: 笔记本电脑， 台式机, Null")
    # 与设备表建关系
    devices = db.relationship('AssetsInfo', lazy='dynamic', backref=db.backref('assets_dict'))
    # 预申请表建关系
    applys = db.relationship('ApplyInfo', lazy='joined', backref=db.backref('assets_dict'))
