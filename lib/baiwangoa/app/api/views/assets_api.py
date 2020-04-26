#
# coding=utf-8

import os
import time
import logging
from flask import request
from .base_api import BaseAPI
from config import Config as gconfig
from lib.baiwangoa.common.utils import to_dict
from lib.baiwangoa.handler import AssetsHP, login_require


logger = logging.getLogger(__name__)


class AssetsAPI(BaseAPI):
    
    @login_require(1)
    def get(self, method=None):
        try:
            dct = to_dict(request.args)
            logger.info('GET: {dct}'.format(dct=dct))
            resp = AssetsHP(method=method, args=dct).run()
            self.response.Resp = resp
            self.response.Result = 'success'
            return self.response.make_response()
        except Exception as e:
            logger.exception(str(e))
            self.response.Result = 'failed'
        return self.response.make_response()
