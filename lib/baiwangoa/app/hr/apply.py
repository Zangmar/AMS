#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import render_template, request, flash, url_for, redirect, session
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import login_require, ApplyHP

logger = logging.getLogger(__name__)


class Apply(MethodView):
    """hr对apply的操作
    
    申请查看权限可以在hr的权限处
    """
    @login_require(1)
    def get(self, method=None):
        try:
            dct = to_dict(request.args)
            # 添加当前hr的id作为查询参数进行查询
            dct['send_employee_id'] = session['user_id']
            logger.info('GET: {dct}'.format(dct=dct))
            # 正常请求，目前为止返回的是pagination对象, 进行分页查询操作
            pagination = ApplyHP(method=method, args=dct).run()
            return render_template('hr/apply/manage.html', pagination=pagination)
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500

    @login_require(1)
    def post(self, method):
        try:
            dct = to_dict(request.form)
            # 添加当前hr的id作为查询参数进行提交
            dct['send_employee_id'] = session['user_id']
            logger.info('POST: {dct}'.format(dct=dct))
            res = ApplyHP(method=method, fields=dct).run()
            flash(res)
            return redirect(url_for('hr.apply'))
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500