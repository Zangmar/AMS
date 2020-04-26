#
# coding=utf-8

import os
import logging
from datetime import datetime
from config import global_config as gconfig
from lib.baiwangoa.common.utils import excel_parser, to_date
from lib.baiwangoa.model.base_db import BaseDB
from lib.baiwangoa.model.models import AssetsInfo, AssetsDict, ApplyInfo, EmployeeInfo

logger = logging.getLogger(__name__)


class AssetsHP(BaseDB):
    """设备相关操作"""

    def __init__(self, method=None, args=None, fields=None):
        """
        :param method: AssetsHp method
        :param args: search params, Dict type
        :param fields: Dict type
        """
        super(AssetsHP, self).__init__()
        self.method = method or 'show_by_page'  # 默认方法
        self.args = args if args else {}  # 查询数据
        self.fields = fields if fields else {}  # 表单数据

    def show_by_page(self):
        """根据条件的资产维护展示"""
        page = int(self.args['page']) if self.args.get('page') else 1
        # 限制字段
        condition_list = []
        if self.args.get('employee_name'):
            vague_condition_tuple = (EmployeeInfo.name.like('%'+self.args['employee_name']+'%'), )
            employee_list = EmployeeInfo.query.filter(*vague_condition_tuple).all()
            employee_id_set = set([employee.id for employee in employee_list])
            condition_list.append(AssetsInfo.employee_id.in_(employee_id_set))
        if self.args.get('code'):
            condition_list.append(AssetsInfo.code==self.args['code'])
        if self.args.get('status'):
            condition_list.append(AssetsInfo.status==self.args['status'])
        if self.args.get('asset_name'):
            code_name_list = (AssetsDict.name.like('%'+self.args['asset_name']+'%'), )
            code_info = AssetsDict.query.filter(*code_name_list).all()
            code_info_set = set(code.id for code in code_info)
            condition_list.append(AssetsInfo.assets_dict_id.in_(code_info_set))
        if self.args.get('serial_num'):
            serial_num_list = (AssetsInfo.sn.like('%'+self.args.get('serial_num')+'%'),)
            serial_info = AssetsInfo.query.filter(*serial_num_list).all()
            serial_info_set = set(serial.id for serial in serial_info)
            condition_list.append(AssetsInfo.id.in_(serial_info_set))
        # query
        if condition_list:
            paginate = AssetsInfo.query.filter(*condition_list).\
                    order_by(AssetsInfo.id.desc()).\
                    paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        else:
            paginate = AssetsInfo.query.\
                    order_by(AssetsInfo.id.desc()).\
                    paginate(page, per_page=gconfig.PER_PAGE_NUMBER, error_out=False)
        # 封装paginate
        renew_items = map(lambda device: MergeTable(device), paginate.items)
        paginate.renew_items = renew_items
        return paginate

    def query_types_name(self):
        """查询子类名

        表: assets_dict
        先获取资产字典表的所有行，然后去重并保持顺序
        return type_names_list"""
        from collections import OrderedDict
        od = OrderedDict()
        types_name_all = AssetsDict.query.with_entities(AssetsDict.type_).all()
        for type_name_tuple in types_name_all:
            if type_name_tuple[0] not in od:
                od[type_name_tuple[0]] = ''
        return od.keys()

    def query_assets_name(self):
        """查询某类的全部资产名
           
        表: assets_dict表
        return assets_name_list, list"""
        type_ = self.args.get('name')
        return map(lambda assets_info: {'id': assets_info.id, 'name': assets_info.name, 'code':assets_info.code}, 
                   AssetsDict.query.filter_by(type_=type_).all())
    
    def query_assets_info(self):
        """assets_info表查询全部入库的某种设备
           
        表: assets_dict
        return asssets_info_list, list
        """
        assets_dict_id =self.args.get('assets_dict_id')
        status = self.args.get('status')
        return map(lambda assets_info: {'id': assets_info.id, 'code': assets_info.code},
                   AssetsInfo.query.filter_by(assets_dict_id=assets_dict_id, status=status).all())

    def add(self):
        """添加一个设备"""
        assets_obj = AssetsInfo()
        # 处理code字段, 根据";"区分
        assets_dict_string = self.fields.pop('assets_dict_string')
        self.fields['assets_dict_id'], pre_code = assets_dict_string.split(';')
        last_code = self.fields.pop('last_code')
        self.fields['code'] = ''.join([pre_code, last_code])
        # add
        self._set_attr(assets_obj, **self.fields)
        self.db.add(assets_obj)
        return '添加成功'

    def add_all(self):
        """批量添加新设备
        
        """
        # file 现根据获取的文件名拿到文件
        filename = self.fields.get('filename')
        path_filename = os.path.join(gconfig.base_path, gconfig.UPLOAD_FOLDER, filename)
        # excel parser 通过路径名直接解析文件, 得到data_list
        data_list = excel_parser(path_filename)  # [list{dict}] 结构
        # count add and fail
        add_count, failed_count = 0, 0
        # failed list
        failed_list = []
        # build device employee dict
        # device dict 
        device_dict = {}
        device_list = AssetsDict.query.with_entities(AssetsDict.id, AssetsDict.name).all()
        for device_tuple in device_list:
            device_dict[device_tuple[1]] = str(device_tuple[0])   # {'mac pro': '1'}
        # employee dict
        employee_dict = {}
        employee_list = EmployeeInfo.query.with_entities(EmployeeInfo.id, EmployeeInfo.name).all()
        for employee_tuple in employee_list:
            employee_dict[employee_tuple[1]] = str(employee_tuple[0])  # {'张三': '2'}
        # exist code
        code_exist_set = set()
        code_list = AssetsInfo.query.with_entities(AssetsInfo.code).all()
        for code_tuple in code_list:
            code_exist_set.add(code_tuple[0])
        # iter data_list
        for data in data_list:
            # obj attrs
            attrs_dict = {}
            # code 检查code是否唯一
            if data[u'资产编码'] in code_exist_set:
                # logger.debug('The excel have a data that code have exist')
                s1 = '编码已存在'
                s2 = ' '.join(data.values())
                failed_count += 1
                failed_list.append(':'.join([s1, s2]))
                continue
            attrs_dict['code'] = data[u'资产编码']
            # assets_dict_id 检查device_name是否存在
            if data[u'设备名'] not in device_dict:
                # logger.debug('The excel have a data that device name have not exist')
                s1 = '设备名不存在'
                s2 = ' '.join(data.values())
                failed_count += 1
                failed_list.append(':'.join([s1, s2]))
                continue
            attrs_dict['assets_dict_id'] = device_dict[data[u'设备名']]
            # to datetime.date format
            if data[u'入库时间']:
                attrs_dict['storage_time'] = to_date(data[u'入库时间'])
            # else:
            # sn
            if data[u'序列号']:
                attrs_dict['sn'] = data[u'序列号']
            # location
            if data[u'库房位置']:
                attrs_dict['location'] = data[u'库房位置']
            # status
            attrs_dict['status'] = data[u'设备状态']
            # employee_id
            if data[u'设备状态']=='2':
                if data[u'使用人'] in employee_dict:
                    attrs_dict['employee_id'] = employee_dict[data[u'使用人']]
                else:
                    s1 = '使用人不存在'
                    s2 = ' '.join(data.values())
                    failed_count += 1
                    failed_list.append(':'.join([s1, s2]))
                    continue
            if data[u'详细信息']:
                attrs_dict['specifications'] = data[u'详细信息']
            # logger 
            logger.info('Multi add data: {}'.format(data))
            assets_obj = AssetsInfo()
            # set attribute
            self._set_attr(assets_obj, **attrs_dict)
            self.db.add(assets_obj, commit=False)
            # code_set add
            code_exist_set.add(attrs_dict['code'])
            add_count += 1
        # commit
        self.db.commit()
        msg = '添加成功, 添加{}条, 失败{}条'.format(add_count, failed_count)
        logger.debug(msg)
        # 添加失败的data
        for i, failed_item in enumerate(failed_list):
            print i, failed_item
        return msg

    def update(self):
        """update
        
        1. assets逻辑: 拿到设备对象
        2. status逻辑: 如果有status: status=any; 如果没有status: 根据是否有使用人判断是否入库
        3. last_employee逻辑: 如果更换使用人，则将当前使用人改为上一个使用人, 更新转移时间
        4. employee逻辑: 判断employee是否存在，不存在说明在仓库，所以存储为None
        5 apply逻辑: 查询到有这个apply，就变换状态
        """
        # 1 assets逻辑: 拿到设备对象
        assets_obj = AssetsInfo.query.filter_by(id=self.fields['id']).first()
        # 2 status逻辑: 如果有status: status=any; 如果没有status: 根据是否有使用人判断是否入库
        if not self.fields.get('status'): 
            self.fields['status'] = 2 if self.fields.get('employee_id') else 1
        # 3 last_employee逻辑: 如果更换使用人，则将当前使用人改为上一个使用人
        employee_id = str(assets_obj.employee_id) if assets_obj.employee_id else ''  # avoid None
        if self.fields.get('employee_id') != employee_id:
            if assets_obj.employee_id:
                # 如果有使用再去查库
                employee = assets_obj.employee
                self.fields['last_employee_name'] = employee.name
                self.fields['last_employee_department'] = employee.department
            else:
                # 上一个使用人是库房
                self.fields['last_employee_name'] = ''
                self.fields['last_employee_department'] = ''
        # 4 employee逻辑: 判断employee是否存在，不存在说明在仓库，所以存储为None
        if not self.fields.get('employee_id'): self.fields['employee_id'] = None
        self._set_attr(assets_obj, **self.fields)
        self.db.commit()  # commit
        # 5 apply逻辑: 查询到有这个apply，就变换状态
        logger.debug('employee_id: {}'.format(assets_obj.employee_id))
        logger.debug('assets_dict_id: {}'.format(assets_obj.assets_dict_id))
        if assets_obj.employee_id and assets_obj.assets_dict_id:
            apply_obj = ApplyInfo.query.filter_by(employee_id=assets_obj.employee_id,
                                                  assets_dict_id=assets_obj.assets_dict_id,
                                                  status='W').first()
            logger.debug('apply_obj: {}'.format(apply_obj))
            if apply_obj:
                apply_obj.status = 'O'  # 更新状态
                self.db.commit()  # commit
        return '更新成功'

    def delete(self):
        """先删除关联的状态转移对象，在删除资产对象"""
        assets = AssetsInfo.query.filter_by(id=self.fields['id']).first()
        self.db.delete(assets)
        return '删除成功'

    def check_code(self):
        """检查编码是否存在"""
        code = self.args.get('code')
        if code and AssetsInfo.query.filter_by(code=code).first():
            return 'exist'
        else:
            return 'no_exist'

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

    def __init__(self, device):
        self.device = device
        self.assets_dict = device.assets_dict
        self.employee = device.employee
