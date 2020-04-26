#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import request, render_template, flash, redirect, url_for
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import login_require, AssetsHP

logger = logging.getLogger(__name__)


class Device(MethodView):
    """admin对device的操作"""

    @login_require(2)
    def get(self, method=None):
        try:
            dct = to_dict(request.args)
            logger.info('GET: {dct}'.format(dct=dct))
            # 正常请求，目前为止返回的是pagination对象, 进行分页查询操作
            pagination = AssetsHP(method=method, args=dct).run()
            return render_template('admin/device/manage.html', pagination=pagination)
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500

    @login_require(2)
    def post(self, method):
        try:
            form = request.form
            dct = to_dict(form)
            self._check_form(dct)  # 表单检查
            logger.info('POST: {dct}'.format(dct=dct))
            res = AssetsHP(method=method, fields=dct).run()
            flash(res)
            return redirect(url_for('admin.device'))
        except ValueError as e:
            logger.error(str(e))
            return render_template('error.html'), 400
        except Exception as e:
            logger.exception(str(e))  # stack exception
            return render_template('error.html'), 500


    def _check_form(self, form):
        """表单检查
        
        主要针对form里面的数据进行检查，
        目前包括对radio的字段进行检查
        """
        if form.get('status') == 'on':
            # 如果传过来的数据为on，那么不改动
            form.pop('status')