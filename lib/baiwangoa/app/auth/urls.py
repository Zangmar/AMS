#
# coding=utf-8

from . import auth as auth_bp

from .main import Main
from .login import Login
from .logout import Logout

auth_bp.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET'])
auth_bp.add_url_rule('/login', view_func=Login.as_view('login'), methods=['GET', 'POST'])
auth_bp.add_url_rule('/logout', view_func=Logout.as_view('logout'), methods=['GET'])
