#!/usr/bin/env python
import sys
from os.path import dirname, abspath, join

from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES =  {
            "default": {
                "ENGINE": 'django.db.backends.sqlite3', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                "NAME": 'test_django_redis_dashboard', # Or path to database file if using sqlite3.
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
        ROOT_URLCONF='tests.urls',
        DEBUG=False,
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

# If we move import to top when raised an error
from django.test.simple import DjangoTestSuiteRunner

class RedisDashboardDjangoTestSuiteRunner(DjangoTestSuiteRunner):

    def setup_test_environment(self, **kwargs):
        super(RedisDashboardDjangoTestSuiteRunner, self).setup_test_environment(**kwargs)

        import subprocess
        redis_config_path = join(dirname(__file__), 'test_redis.conf')
        print(redis_config_path)
        #result = subprocess.Popen('redis-server %s' % redis_config_path)


def setup_run_tests(*test_args):
    if not test_args:
        test_args = ['redis_dashboard']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    test_runner = RedisDashboardDjangoTestSuiteRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(test_args)

    #failures = run_tests(test_args, verbosity=1, interactive=True)
    #failures = RedisDashboardDjangoTestSuiteRunner().run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    setup_run_tests(*sys.argv[1:])
