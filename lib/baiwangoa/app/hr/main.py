#
# coding=utf-8

from flask.views import MethodView
from flask import render_template
from lib.baiwangoa.handler import login_require


class Main(MethodView):

    @login_require(1)
    def get(self):
        return render_template('hr/main.html')
