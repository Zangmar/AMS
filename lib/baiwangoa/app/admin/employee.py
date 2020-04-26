#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, jsonify
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import login_require, EmployeeHP

logger = logging.getLogger(__name__)


class Employee(MethodView):
    """admin对所有employee的操作"""

    @login_require(2)
    def get(self, method=None):
        try:
            dct = to_dict(request.args)
            logger.info('GET: {dct}'.format(dct=dct))
            # 正常请求，目前为止返回的是pagination对象, 进行分页查询操作
            pagination = EmployeeHP(method=method, args=dct).run()
            return render_template('admin/employee/manage.html', pagination=pagination)
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500

    @login_require(2)
    def post(self, method):
        try:
            form = request.form
            dct = to_dict(form)
            self._check_form(dct)
            logger.info('POST: {dct}'.format(dct=dct))
            res = EmployeeHP(method=method, fields=dct).run()
            flash(res)
            return redirect(url_for('admin.employee'))
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500

    def _check_form(self, form):
        """表单检查
        
        主要针对form里面的数据进行检查，
        目前包括对radio的字段进行检查
        """
        if form.get('permission') == 'on':
            form.pop('permission')
        if form.get('is_work') == 'on':
            form.pop('is_work')
