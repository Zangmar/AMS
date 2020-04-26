#
# coding=utf-8

from datetime import datetime
from werkzeug.security import check_password_hash
from . import ApplyInfo
from .base_model import BaseMix
from lib.baiwangoa.model import db


class EmployeeInfo(db.Model, BaseMix):
    """员工信息表"""
    __tablename__ = 'employee_info'
    phone = db.Column(db.String(15), unique=True, nullable=False, comment="电话 用户唯一id")
    password = db.Column(db.String(100), nullable=True, comment="密码")
    permission = db.Column(db.SmallInteger, default=1, comment="权限 3种：admin=3, hr=2, normal=1")
    name = db.Column(db.String(40), index=True, nullable=False, comment="员工姓名")
    entry_time = db.Column(db.Date, nullable=True, comment="入职时间 人力手动填写")
    department = db.Column(db.String(40), nullable=True, comment="所属部门")
    # 注: Boolean到MySQL中就变成TinyInteger了
    is_work = db.Column(db.String(1), default='1', nullable=True, comment="是否在职 1:在职, 0:离职")
    # 与apply_info表建立关系, 员工的全部申请
    applys = db.relationship('ApplyInfo', lazy='joined', foreign_keys=[ApplyInfo.employee_id],
                             backref=db.backref('employee'))
    # 与apply_info表建立关系, 申请发送者的全部申请
    send_applys = db.relationship('ApplyInfo', lazy='joined', foreign_keys=[ApplyInfo.send_employee_id], 
                                  backref=db.backref('send_employee'))
    # 与assets_info建立关系
    devices = db.relationship('AssetsInfo', lazy='dynamic', backref=db.backref('employee'))


    def check_password(self, password):
        """检查hash过的password

        :return Bool type
        """
        return check_password_hash(self.password, password)



