#
# coding=utf-8

import os
import sys
from flask_script import Manager
from db_manager import db_manager
from lib.baiwangoa.app import create_app

reload(sys)
sys.setdefaultencoding('utf8')

app = create_app(os.getenv('TEMP_LOCAL_CONFIG') or 'development')
manager = Manager(app)

manager.add_command('db', db_manager)


@manager.command
def runserver():
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)


def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()

