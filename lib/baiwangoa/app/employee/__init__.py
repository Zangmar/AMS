#
# coding=utf-8

from flask import Blueprint

employee = Blueprint('employee', __name__)

from .urls import *
