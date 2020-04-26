#
# coding=utf-8

from flask import Blueprint

hr = Blueprint('hr', __name__)

from .urls import *
