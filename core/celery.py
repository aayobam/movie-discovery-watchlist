import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
APP = Celery("core")
APP.config_from_object("django.conf:settings", namespace="CELERY")
APP.autodiscover_tasks()
