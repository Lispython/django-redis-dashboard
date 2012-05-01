Welcome to django_redis_dashboard's documentation!
==================================================

django_redis_dashboard application for monitoring redis servers which
used by application.


Usage
-----





INSTALLATION
------------

1. To use django_redis_dashboard  use pip or easy_install:

`pip install django_redis_dashboard`

or

`easy_install django_redis_dashboard`


2. Add redis_dashboard to your ``INSTALLED_APPS`` setting::

       INSTALLED_APPS = (
           # ...
           'redis_dashboard',
       )


3. Add the urls to your url configuration::

       urlpatterns = patterns('',
           # ...
           (r'^redis-dashboard/', include('redis-dashboard.urls')),
       )
4. Configure you redis servers::

      REDIS = {
           'default': {
	              'HOST': '127.0.0.1',
                  'PORT': 6379,
                  'DB': 2
		   },
           'slave': {
		          'HOST': '127.0.0.1',
                  'PORT': 6378,
				  'DB': 3
           }
      }


CONTRIBUTE
----------

Fork https://github.com/Lispython/django-redis-dashboard/ , create commit and pull request.


SEE ALSO
--------

-  `python pypi`_.

.. _`python pypi`: http://pypi.python.org
