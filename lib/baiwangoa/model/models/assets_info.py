#
# coding=utf-8

from datetime import datetime
from .base_model import BaseMix
from lib.baiwangoa.model import db


class AssetsInfo(db.Model, BaseMix):
    """设备信息表."""
    __tablename__ = 'assets_info'
    code = db.Column(db.String(50), unique=True, comment="设备唯一键: 设备编码")
    sn = db.Column(db.String(100), default='', nullable=True, comment="设备sn序列号")
    # specification: 设备具体规格记录 ex: 显卡，CPU 等等
    status = db.Column(db.String(1), default='1', comment="设备状态 ex: 1入库，2出库，3维修中")
    storage_time = db.Column(db.Date, default=datetime.now, comment="入库时间")
    location = db.Column(db.String(80), default='', nullable=True, comment="仓库位置")
    # last_employee info
    last_employee_name = db.Column(db.String(40), default='', nullable=True, comment="上一个使用人姓名")
    last_employee_department = db.Column(db.String(40), default='', nullable=True, comment="上一个使用人地址")
    # 外键关联employee_info表, 关联上一个使用人， 可以为空，当为空时说明设备在仓库
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_info.id'), nullable=True, comment="员工外键 可以为空，当为空时说明设备在仓库")
    # 外键关联资产字典表
    assets_dict_id = db.Column(db.Integer, db.ForeignKey('assets_dict.id'), nullable=False, comment="字典表外键")
