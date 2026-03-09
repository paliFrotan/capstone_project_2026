import os

SECRET_KEY = 'django-insecure-$2xwdvba6vik72b-%ztyx!x59lx&o*4!8wz0su-k09_4&h9)r8'
DATABASE_URL='postgresql://neondb_owner:npg_Pv0wjW3UkYNl@ep-summer-flower-aly8g4zz.c-3.eu-central-1.aws.neon.tech/zebra_city_smash_918238'
os.environ.setdefault('SECRET_KEY', SECRET_KEY)
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('ALLOWED_HOSTS', '127.0.0.1')
os.environ.setdefault('DATABASE_URL', DATABASE_URL)
