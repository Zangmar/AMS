#
# coding=utf-8

from . import employee as employee_bp

from .main import Main

employee_bp.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET'])
