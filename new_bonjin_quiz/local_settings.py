import os
from pathlib import Path

#settings.pyからそのままコピー
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'p(32m7r(3*#b2rw_d!8%$tpo*ir#q%$)dqw*j-sqzfbr(aq#-x'

#settings.pyからそのままコピー
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'new_bonjin_quiz',
        'USER': 'postgres',
        'PASSWORD': 'mecmecmec',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

DEBUG = True #ローカルでDebugできるようになります