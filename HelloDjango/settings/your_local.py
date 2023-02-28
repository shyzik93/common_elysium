# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'secret_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            # https://django-mysql.readthedocs.io/en/latest/checks.html#django-mysql-w003-utf8mb
            'init_command': 'SET innodb_strict_mode=1; SET sql_mode=\'STRICT_TRANS_TABLES\'',
            'charset': 'utf8mb4',
        }
    }
}
    
SCHEMA = 'http'
