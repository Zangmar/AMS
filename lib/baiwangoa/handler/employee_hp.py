#
# coding=utf-8

import logging
from werkzeug.security import generate_password_hash
from config import global_config as gconfig
from lib.baiwangoa.model.base_db import BaseDB
from lib.baiwangoa.model.models import EmployeeInfo

logger = logging.getLogger(__name__)


class EmployeeHP(BaseDB):
    """Employee DB handler"""

    def __init__(self, method=None, args=None, fields=None):
        """
        :param method: EmployeeHP method
        :param args: search params, Dict type, include 'phone', 'page', etc
        :param fields: Dict type, include 'id'; 'phone'; 'password'; 'permission'; 'name'; 'entry_time';
                       'department'; 'is_work'
        """
        super(EmployeeHP, self).__init__()
        self.method = method or 'show_by_page'  # 默认方法
        self.args = args if args else {}  # 查询数据
        self.fields = fields if fields else {}  # 表单数据

    def show_by_page(self):
        """根据条件的员工维护展示
        
        return pagination_obj of page number of employee
        """
        page = int(self.args['page']) if self.args.get('page') else 1  # 默认page
        # 限制字段
        condition_list = []
        if self.args.get('name'):
            condition_list.append(EmployeeInfo.name.like(self.args['name']+'%'))
        if self.args.get('phone'):
            condition_list.append(EmployeeInfo.phone==self.args['phone'])
        # query
        if condition_list:
            paginate = EmployeeInfo.query.filter(*condition_list).\
                order_by(EmployeeInfo.id.desc()).\
                paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        else:
            paginate = EmployeeInfo.query.\
                    order_by(EmployeeInfo.id.desc()).\
                    paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        return paginate

    def check_phone(self):
        """return result, string"""
        phone = self.args.get('phone')
        if phone and EmployeeInfo.query.filter_by(phone=phone).first():
            return 'exist'
        else:
            return 'no_exist'

    def query_employee_info(self):
        """ 查询员工信息
        
        return empoyee_list, [{}]"""
        query_args_dict = {'name': self.args.get('name')}  # query arguments dict
        # 如果需要限制员工是否在职
        if self.args.get('is_work'):
            query_args_dict['is_work'] = self.args['is_work']
        return map(lambda employee: {'id': employee.id,
                                     'name': employee.name,
                                     'department': employee.department,
                                     'phone': employee.phone
                                     }, EmployeeInfo.query.filter_by(**query_args_dict).all())

    def add(self):
        employee_obj = EmployeeInfo()
        self.fields.pop('id')  # id automatic add
        self.fields['password'] = generate_password_hash(self.fields['password'])  # hash encode
        self._set_attr(employee_obj, **self.fields)
        self.db.add(employee_obj)
        logger.info('add success')
        return '添加成功'

    def update(self):
        if self.fields.get('phone'):
            self.fields.pop('phone')  # not update phone
        if self.fields.get('password'):
            self.fields.pop('password')  # not update passowrd, 密码只能重置
        employee_obj = EmployeeInfo.query.filter_by(id=self.fields['id']).first()
        self._set_attr(employee_obj, **self.fields)
        self.db.commit()  # commit
        logger.info('update success')
        return '更新成功'

    def delete(self):
        """删除员工

        如果员工有设备会报错， 因为这样说明员工手上还有公司设备
        """
        employee_obj = EmployeeInfo.query.filter_by(id=self.fields['id']).first()
        self.db.delete(employee_obj)
        logger.info('delete success')
        return '删除成功'

    def response(self):
        """
        反射self的method

        先去判断该method是否这self的属性中并且不是魔法方法
        :return: self.method
        """
        if self.method not in filter(lambda item: not item.startswith('_'), dir(self)):
            raise ValueError('Without this method-{}'.format(self.method))
        return getattr(self, self.method)()
