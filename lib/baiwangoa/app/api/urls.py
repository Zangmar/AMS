#
# -*- coding:utf-8 -*-

"""
API URL Configuration
"""

from . import api

from .views import EmployeeAPI
from .views import AssetsAPI
from .views import UploadAPI


api.add_url_rule('/employee/<string:method>', view_func=EmployeeAPI.as_view('employee_api'), methods=['POST', 'GET'])
api.add_url_rule('/assets/<string:method>', view_func=AssetsAPI.as_view('assets_api'), methods=['POST', 'GET'])
api.add_url_rule('/upload', view_func=UploadAPI.as_view('upload_api'), methods=['POST'])
