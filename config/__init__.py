#
# -*- coding:utf-8 -*-

import os
import re
import yaml
from datetime import timedelta
from logging.config import fileConfig

base_path = os.path.dirname(os.path.realpath(__file__)) + '/..'


def logging_config(logdir, level='INFO', log_name='ITSupport'):

    if not os.path.isdir(logdir) and not os.path.exists(logdir):
        os.makedirs(logdir)

    kw_args = {'log_name': log_name}
    LOG_LEVEL = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']
    if level not in LOG_LEVEL:
        raise ValueError('bad logging level!')
    else:
        kw_args['level'] = level

    kw_args['info_log_path'] = os.path.join(logdir, log_name + '_info.log')
    kw_args['debug_log_path'] = os.path.join(logdir, log_name + '_debug.log')

    if level == 'DEBUG':
        kw_args['log_handlers'] = 'file_DEBUG, console'
    else:
        kw_args['log_handlers'] = 'file_INFO'

    with open(os.path.join(base_path, 'config/log.conf.template'), 'r') as fr:
        data = fr.read()
        for k, v in kw_args.items():
            data = re.sub('{{\ *%s\ *}}' % k, v, data)

        with open(os.path.join(base_path, 'config/log.conf'), 'w') as fw:
            fw.write(data)

    fileConfig(os.path.join(base_path, 'config/log.conf'))


class Config:
    def __init__(self, config_file=None):
        self.base_path = base_path
        self.config_data = {}

        if config_file is None:
            config_file = os.path.join(base_path, 'config/baiwangoa.yaml')
        with open(config_file, 'r') as f:
            self.config_data = yaml.load(f)

        self.DB_LINK = os.environ.get('DB_LINK') \
            or self.db_link(self.config_data.get('DB_LINK'))

        if not self.config_data:
            raise ValueError("Not Found Config")

    def __getattr__(self, item):
        return self.config_data.get(item)

    @staticmethod
    def db_link(db_link_dict):
        db_type = db_link_dict.get('DB_TYPE', ' ').lower()
        db_link = None
        if db_type == 'mysql':
            db_link = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8'.format(
                user=db_link_dict.get('User', ' '),
                passwd=db_link_dict.get('Passwd', ' '),
                host=db_link_dict.get('Host', ' '),
                port=db_link_dict.get('Port', 3306),
                db_name=db_link_dict.get('DB_Name', ' ')
            )
        else:
            if db_type == 'sqlite':
                db_link = 'sqlite+pysqlite:///{path}'.format(
                    path=db_link_dict.get('DB_PATH', 'taishan.sqlite')
                )

        return db_link

    # sqlchemy config 追踪对象的修改并且发送信号
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    import binascii
    SECRET_KEY = binascii.hexlify(os.urandom(30))
    # session invalid during
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)


# global config singleton
global_config = Config()


class DevelopmentConfig(Config):
    """开发Config"""
    DEBUG = True
    logging_config('/tmp/baiwangoa/log')

class LocalConfig(Config):
    """本地测试Config"""
    DEBUG = True
    # logging_config('log_files')
    logging_config('/tmp/baiwangoa/log')


config = {
    'development': DevelopmentConfig,
    'local': LocalConfig
}
