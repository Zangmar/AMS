#
# coding=utf-8

import logging
from flask.views import MethodView
from flask import redirect, url_for, render_template, flash
from lib.baiwangoa.handler import login_require, logout_user

logger = logging.getLogger(__name__)


class Logout(MethodView):
    """logout method"""

    @login_require()
    def get(self):
        try:
            logger.info('I got Logout get')
            logout_user()
            return redirect(url_for('auth.login'))
        except Exception as e:
            logger.exception(str(e))
            return render_template('error.html'), 500
