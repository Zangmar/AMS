import os
import sys
from lib.baiwangoa.app import create_app
reload(sys)
sys.setdefaultencoding('utf8')

app = create_app(os.getenv('LOCAL_CONFIG') or 'development')


def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
