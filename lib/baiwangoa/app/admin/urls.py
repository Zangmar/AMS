#
# coding=utf-8

from . import admin as admin_bp

from .main import Main
from .employee import Employee
from .apply import Apply
from .device import Device


def register_api(view, endpoint, url, pk='id', pk_type='string'):
    """ flask official recommend / and /<> method

    :param view: view function
    :param endpoint: endpoint
    :param url: url
    :param pk: 变量
    :param pk_type: 变量类型
    :return:
    """
    view_func = view.as_view(endpoint)
    admin_bp.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    admin_bp.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'POST'])


admin_bp.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET'])
register_api(Employee, 'employee', '/employee', pk='method')
register_api(Device, 'device', '/device', pk='method')
register_api(Apply, 'apply', '/apply', pk='method')
