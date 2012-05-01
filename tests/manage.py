#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES =  {
            "default": {
                "ENGINE": 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                "NAME": 'debug_django_redis_dashboard', # Or path to database file if using sqlite3.
                "USER": '', # Not used with sqlite3.
                "PASSWORD": '', # Not used with sqlite3.
                "HOST": '', # Set to empty string for localhost. Not used with sqlite3.
                "PORT": '', # Set to empty string for default. Not used with sqlite3.
                }
            },
        # HACK: this fixes our threaded runserver remote tests
        # TEST_DATABASE_NAME='test_django_redis_dashboard'
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',

            # Switch on redis_dashboard
            'django.contrib.contenttypes',
            'redis_dashboard'
        ],
        ROOT_URLCONF='urls',
        DEBUG=True,
        DATE_INPUT_FORMATS=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
                            '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
                            '%B %d, %Y', '%d %B %Y', '%d %B, %Y'),
        SITE_ID=1,
        REDIS_DBS = {
            'default': {
                'HOST': '127.0.0.1',
                'PORT': 6479,
                'DB': 1
                },
            'slave': {
                'HOST': '127.0.0.1',
                'PORT': 6479,
                'DB': 2
                },
            }
        )

if __name__ == '__main__':
    from django.core.management import execute_manager
    execute_manager(settings)


