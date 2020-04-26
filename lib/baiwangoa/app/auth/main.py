#
# coding=utf-8

from flask.views import MethodView
from flask import redirect, url_for, session
from lib.baiwangoa.handler import LoginHP


class Main(MethodView):
    """Main page view method"""

    def get(self):
        if session.get('user_id'):
            res = LoginHP(method='choose_main', data={'permission':session.get('permission')}).run()
            return redirect(url_for('{name}.main'.format(name=res)))
        else:
            return redirect(url_for('auth.login'))  # main page redirect to login