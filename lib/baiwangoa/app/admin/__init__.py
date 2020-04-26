#
# coding=utf-8

from flask import Blueprint

admin = Blueprint('admin', __name__)

from .urls import *  # 需要执行，所以需要导入全部
