#
# coding=utf-8

import logging
from datetime import datetime
from werkzeug.security import generate_password_hash
from config import global_config as gconfig
from lib.baiwangoa.model.base_db import BaseDB
from lib.baiwangoa.model.models import ApplyInfo, AssetsInfo, EmployeeInfo

logger = logging.getLogger(__name__)


class ApplyHP(BaseDB):
    """申请相关操作"""

    def __init__(self, method=None, args=None, fields=None):
        """
        :param method: ApplyHP method
        :param args: search params, Dict type
        :param fields: Dict type
        """
        super(ApplyHP, self).__init__()
        self.method = method or 'show_by_page'  # 默认方法
        self.args = args if args else {}  # 查询数据
        self.fields = fields if fields else {}  # 表单数据

    def show_by_page(self):
        """申请维护展示

        可以根据申请的hr进行返回查询结果
        return: pagination_obj of page_size number of applys"""
        page = int(self.args['page']) if self.args.get('page') else 1  # 查询页码
        # 限制字段
        condition_list = []
        if self.args.get('employee_name'):
            vague_condition_tuple = (EmployeeInfo.name.like(self.args['employee_name']+'%'), )
            employee_list = EmployeeInfo.query.filter(*vague_condition_tuple).all()
            employee_id_set = set([employee.id for employee in employee_list])
            condition_list.append(ApplyInfo.employee_id.in_(employee_id_set))
        # 限制发送申请人
        if self.args.get('send_employee_id'):
            condition_list.append(ApplyInfo.send_employee_id==self.args['send_employee_id'])
        # query
        if condition_list:
            paginate = ApplyInfo.query.filter(*condition_list).\
                order_by(ApplyInfo.id.desc()).\
                paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        else:
            paginate = ApplyInfo.query.\
                    order_by(ApplyInfo.id.desc()).\
                    paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        # 封装paginate
        renew_items = map(lambda device: MergeTable(device), paginate.items)
        paginate.renew_items = renew_items
        return paginate

    def add(self):
        apply_obj = ApplyInfo()
        self._set_attr(apply_obj, **self.fields)
        self.db.add(apply_obj)
        return '添加成功'

    def delete(self):
        apply_obj = ApplyInfo.query.filter_by(id=self.fields['id']).first()
        self.db.delete(apply_obj)
        return '删除成功'

    def handle(self):
        """处理申请方法  
        
        考虑原子性
        1. 将设备与员工关联
        2. 更改设备状态和上一个员工信息
        3. 更改申请状态
        """
        # 1
        assets_info_id = self.fields.get('assets_info_id')
        assets_info = AssetsInfo.query.filter_by(id=assets_info_id).first()
        assets_info.employee_id = self.fields.get('employee_id')
        # 2, 上一个员工一定是在库中
        assets_info.status = '2'
        assets_info.last_employee_name = ''
        assets_info.last_employee_department = ''
        # 3
        apply_id = self.fields.get('apply_id')
        apply_info = ApplyInfo.query.filter_by(id=apply_id).first()
        apply_info.status = 'O'
        # commit
        self.db.commit()  # update --> apply_info, assets_info
        return '申请处理成功'

    def add_apply_employee(self):
        """添加申请与员工
        
        考虑原子性
        1 fields中先pop出非employee的字段
        2 添加员工 
        3 添加申请并关联该员工
        """
        # 1 fields里只有员工的信息
        assets_dict_id = self.fields.pop('assets_dict_id')
        send_employee_id = self.fields.pop('send_employee_id')
        # 2
        employee_info = EmployeeInfo()
        # 新员工没有密码，默认为手机号
        self.fields['password'] = generate_password_hash(self.fields['phone']) 
        self._set_attr(employee_info, **self.fields)
        self.db.add(employee_info, commit=False)  # 原子性
        self.db.flush()  # 预提交数据
        # 3
        apply_info = ApplyInfo()
        apply_info.employee_id = employee_info.id
        apply_info.assets_dict_id = assets_dict_id
        apply_info.send_employee_id = send_employee_id
        # commit
        self.db.add(apply_info)
        return '添加申请成功'

    def response(self):
        """
        反射self的method

        先去判断该method是否这self的属性中并且不是魔法方法
        :return: self.method
        """
        if self.method not in filter(lambda item: not item.startswith('_'), dir(self)):
            raise ValueError('Without this method-{}'.format(self.method))
        return getattr(self, self.method)()


class MergeTable(object):
    """封装表对象与其关系"""

    def __init__(self, apply_):
        self.apply = apply_
        self.assets_dict = apply_.assets_dict
        self.employee = apply_.employee
