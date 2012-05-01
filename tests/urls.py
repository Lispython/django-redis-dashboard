#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from django.conf.urls.defaults import url, patterns, include
from django.contrib import admin

from redis_dashboard.views import redis_dashboard_admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^redis-dashboard/', include(redis_dashboard_admin.urls)),
    )
