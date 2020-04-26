#
# coding=utf-8

from flask.views import MethodView
from flask import render_template
from lib.baiwangoa.handler import login_require


class Main(MethodView):

    @login_require(2)
    def get(self):
        return render_template('admin/main.html')
