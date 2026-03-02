#!/bin/bash

set -e

if pgrep -f "ego-toolbox" > /dev/null; then
    echo "ego-toolbox is running"
    pgrep -f "ego-toolbox" | xargs kill
    # 谨慎使用 kill -9：SIGKILL信号（-9）强制进程立即终止，不给进程任何清理资源的机会
    echo "ego-toolbox is stopped"
fi


# source /app/ego-toolbox/.venv/bin/activate
cd /app/ego-toolbox/ego/
/app/ego-toolbox/.venv/bin/gunicorn mysite.wsgi:application -c gunicorn_conf.py -D

echo "ego-toolbox is started"