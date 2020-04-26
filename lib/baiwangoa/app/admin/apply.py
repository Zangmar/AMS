#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import render_template, request, flash, url_for, redirect
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import login_require, ApplyHP

logger = logging.getLogger(__name__)


class Apply(MethodView):
    """admin对device的操作
    
    申请查看权限可以在hr的权限处
    """

    @login_require(2)
    def get(self, method=None):
        try:
            dct = to_dict(request.args)
            logger.info('GET: {dct}'.format(dct=dct))
            # 正常请求，目前为止返回的是pagination对象, 进行分页查询操作
            pagination = ApplyHP(method=method, args=dct).run()
            return render_template('admin/apply/manage.html', pagination=pagination)
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500

    @login_require(2)
    def post(self, method):
        try:
            form = request.form
            dct = to_dict(form)
            logger.info('POST: {dct}'.format(dct=dct))
            res = ApplyHP(method=method, fields=dct).run()
            flash(res)
            return redirect(url_for('admin.apply'))
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500