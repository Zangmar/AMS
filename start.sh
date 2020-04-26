#!/bin/bash
source ~/.bashrc
shell_path=$(cd `dirname $0`;pwd)
cd $shell_path
option=$1

function _install()
{
    pip install -r $shell_path/requirements.txt
}

function _start()
{
    echo "start it_support"
    uwsgi -d $shell_path/httplog.log --ini $shell_path/uwsgi.ini
}

function _stop()
{
    echo "stop it_support"
    pid=`cat $shell_path/uwsgi.pid`
    kill -3 $pid
    while test -n "`ps -f --pid $pid  --no-heading`"
    do
        sleep 0.1
    done
}

function _creat_db()
{
    python $shell_path/web_service.py db db_init
}

function _start_all()
{
    _creat_db
    sleep 1
    _start
}

case "$option" in
    "install" )
        _install
    ;;
    "createdb" )
        _creat_db
    ;;
    "start" )
        _start
    ;;
    "start-all" )
        _start_all
    ;;
    "stop" )
        _stop
    ;;
   "restart" )
        _stop
        _start
    ;;
    *)
        echo "Usage: start.sh [option]"
        echo ""
        echo "  install : install it_support"
        echo "  createdb : auto createdb"
        echo "  start : start it_support"
        echo "  start-all : start it_support and auto create db"
        echo "  stop : stop it_support"
        echo "  restart : restart it_support"
    ;;

esac
