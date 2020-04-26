#
# coding=utf-8

from flask.views import MethodView
from flask import render_template


class Main(MethodView):

    def get(self):
        return render_template('employee/main.html')