#
# coding=utf-8

from datetime import datetime
from .base_model import BaseMix
from lib.baiwangoa.model import db


class ApplyInfo(db.Model, BaseMix):
    """员工申请表.

    注意: 提交申请时候, 如果没有这个员工, 那么会先在employee表中创建, 再在apply表中创建.
    """
    __tablename__ = 'apply_info'
    apply_time = db.Column(db.Date, default=datetime.now, comment="申请时间")
    status = db.Column(db.String(2), default='W', comment="申请状态 W 未受理；S 受理中；O 已完成")
    # 外键关联employee_info表, 具体使用人
    employee_id = db.Column(db.Integer, db.ForeignKey('employee_info.id'), nullable=True, comment="员工表外键, 具体使用人")
    # 外键关联assets_dict表
    assets_dict_id = db.Column(db.Integer, db.ForeignKey('assets_dict.id'), nullable=True, comment="资产表外键")
    # 外键关联employee_info表, 申请发送者
    send_employee_id = db.Column(db.Integer, db.ForeignKey('employee_info.id'), nullable=True, comment="员工表外键 申请发送者")
    # 创建联合索引
    __table_args__ = (
        db.Index('ix_employee_assets_dict_id', 'employee_id', 'assets_dict_id'),  # 员工id与字典表id
        db.Index('ix_send_employee_employee_id', 'send_employee_id', 'employee_id')  # 发送申请人与申请人
    )
