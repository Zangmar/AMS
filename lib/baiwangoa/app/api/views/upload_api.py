#
# coding=utf-8

import os
import time
import logging
from flask import request
from config import global_config as gconfig
from .base_api import BaseAPI
from lib.baiwangoa.handler import login_require


logger = logging.getLogger(__name__)


class UploadAPI(BaseAPI):

    @login_require(2)
    def post(self):
        try:
            file_obj = request.files.get('file_stream')
            define_name = request.form.get('define_name')
            logger.info('FileStream name: {}, DifineName: {}'.format(file_obj.filename, define_name))

            # 上传文件
            # 获取可以存储的文件名
            if '.' not in file_obj.filename:
                # check . in filename
                raise Exception("'.' not in filename")
            file_suffix = file_obj.filename.rsplit('.', 1)[1].lower()
            if file_suffix not in gconfig.ALLOWED_EXTENSIONS:
                # check filename if illegal
                raise Exception("filename have illegal suffix")
            # default version
            version = time.strftime('%Y%m%d%H%M%S', time.localtime())
            # default save_name
            save_name = "{define_name}@{version}.{file_suffix}".format(
                define_name=define_name,
                version=version,
                file_suffix=file_suffix
            )
            # build path and file
            path_save_name = os.path.join(gconfig.base_path, gconfig.UPLOAD_FOLDER, save_name)
            # save
            file_obj.save(path_save_name)
            file_obj.close()  # 不知道需不需要关闭
            logger.debug('FILE save path: {}'.format(path_save_name))

            self.response.Resp = save_name
            self.response.Result = 'success'
        except IOError as e:
            logger.exception(str(e))
            self.response.Result = 'failed'
        except Exception as e:
            logger.exception(str(e))
            self.response.Result = 'failed'
        return self.response.make_response()
    
    