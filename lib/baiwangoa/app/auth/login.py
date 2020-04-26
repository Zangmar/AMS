#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import request, url_for, redirect, render_template, flash
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import LoginHP, login_user
from lib.baiwangoa.model.models import EmployeeInfo

logger = logging.getLogger(__name__)


class Login(MethodView):
    """login method"""

    def get(self):
        return render_template('auth/login.html')

    def post(self):
        try:
            dct = to_dict(request.form)
            res = LoginHP(method='validate', data=dct).run()
            if res:
                # return redirect(url_for('{name}.main'.format(name=res)))
                return redirect('/')
            else:
                flash('您输入的用户名或密码有误，请从新输入')
                return redirect(url_for('auth.login'))
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500



