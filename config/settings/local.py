import config.settings.db as db
import environ


from .base import *

env = environ.Env()
DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = db.POSTGRESQL

STATIC_URL = "static/"