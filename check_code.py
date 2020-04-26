#
# -*- coding:utf-8 -*-
"""
 在git commit 前务必执行该脚本
 确保正确安装了 git、pylint
"""

import os
import sys
from config import base_path

reload(sys)
sys.setdefaultencoding('utf8')

#TERMINAL_CHAR = 'gbk'
TERMINAL_CHAR = 'utf8'


def print_cn_win(msg):
    msg = msg.decode('utf8').encode(TERMINAL_CHAR)
    print(msg)


def print_cn_linux(msg):
    print(msg)


if 'win' in sys.platform:
    print_cn = print_cn_win
else:
    print_cn = print_cn_linux


def get_changes():
    changes = os.popen('git status -s')
    changes = changes.readlines()
    changes = [line.split()[-1].strip() for line in changes if line.endswith('.py\n')]
    return changes


def check_code_by_pylint(change_list):
    rcfile = os.path.join(base_path, 'pylint.conf')
    file_list = ' '.join(change_list)

    print_cn("=" * 23 + "详情" + "=" * 23)
    details = os.popen('pylint --rcfile={} {}'.format(rcfile, file_list)).readlines()
    rated = details[-2].replace('Your code has been rated at ', '').split('/10')[0]
    for detail in details:
        print_cn(detail.strip())
    if float(rated) < 8:
        print_cn("=" * 60)
        print_cn("\t" * 3 + "!!!!!    请注意     !!!!!" + "\t" * 3)
        print_cn("\t" * 3 + "代码质量过低,请修改后再提交" + "\t" * 3)
        print_cn("\t" * 3 + "!!!!!    请注意     !!!!!" + "\t" * 3)
        print_cn("=" * 60)
        print_cn('\n')

    errors = os.popen('pylint --rcfile={} -d W,C,R {}'.format(rcfile, file_list)).readlines()
    if len(errors) > 4:
        print_cn("=" * 25 + "请重点关注" + "=" * 25)
    for e in errors:
        if e.startswith('----'):
            break
        print_cn(e.strip())

    if len(errors) > 4:
        print_cn("=" * 60)


def main():
    os.chdir(base_path)
    change_list = get_changes()
    if change_list:
        check_code_by_pylint(change_list)


if __name__ == '__main__':
    main()
