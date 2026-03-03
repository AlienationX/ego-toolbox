# gunicorn mysite.wsgi:application -c gunicorn_config.py

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

bind = "127.0.0.1:8081"
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 3
worker_class = "gthread"  # 或 "gevent"
threads = 4
timeout = 120
loglevel = "info"
accesslog = "/var/log/gunicorn/ego-toolbox/access.log"
errorlog = "/var/log/gunicorn/ego-toolbox/error.log"

Path(accesslog).parent.mkdir(parents=True, exist_ok=True)
Path(errorlog).parent.mkdir(parents=True, exist_ok=True)
