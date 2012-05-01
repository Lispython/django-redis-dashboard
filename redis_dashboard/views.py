#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
redis_dashboard.views
~~~~~~~~~~~~~~~~~~~~~

Module provide web graphic interface views

:copyright: (c) 2012 by Alexandr Sokolovskiy (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""


from functools import update_wrapper

from redis import Redis
from django.contrib.admin.sites import AdminSite
from django.utils.functional import Promise
from django.utils.encoding import force_unicode
from django.utils import simplejson
from django.shortcuts import render
from django.http import HttpResponse

from redis.exceptions import ConnectionError

from .common import redis_pool


class LazyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj


class JSONResponse(HttpResponse):
    """
    A simple subclass of ``HttpResponse`` which makes serializing to JSON easy.
    """
    def __init__(self, object, **kwargs):
        content = simplejson.dumps(object, cls=LazyEncoder)
        super(JSONResponse, self).__init__(content, mimetype='application/json', **kwargs)


def ajax_request(func):
    """
    If view returned serializable dict, returns JsonResponse with this dict as content.

    example:

        @ajax_request
        def my_view(request):
            news = News.objects.all()
            news_titles = [entry.title for entry in news]
            return {'news_titles': news_titles}
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            try:
                response = func(request, *args, **kwargs)
            except Exception, ex:
                response = {'success': False, 'code': 500, 'message': ex}
        else:
            response = {'success': False, 'code': 403, 'message': 'Accepts only POST request'}
        if isinstance(response, dict):
            return JSONResponse(response)
        else:
            return response
    return wrapper


class RedisDashboardAdminSite(AdminSite):
    index_template = "redis_dashboard/index.html"

    def __init__(self, name, *args, **kwargs):
        super(RedisDashboardAdminSite, self).__init__(name, *args, **kwargs)
        self.app_name = "redis_dashboard_admin"

    def get_urls(self):

        from django.conf.urls.defaults import patterns, url

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = patterns('',
            url(r'^main/$', wrap(self.main_view), name='index'),
            url(r'details/(?P<alias>\w+)/$', wrap(self.details_view), name='details'),
            url(r'execute-command/$', wrap(self.execute_command), name='execute-command'))
        return urls

    def details_view(self, request, alias, *args, **kwargs):
        connection = redis_pool[alias]
        if not isinstance(connection, Redis):
            redis_params = None
        else:
            redis_params = connection.connection_pool.connection_kwargs

        return render(request, "redis_dashboard/details.html",
                      {'alias': alias, 'alias_params': redis_params,
                       'info': connection.info(),
                       'connection': connection})

    def execute_command(self, request):
        command = request.POST.get('command')
        alias = request.POST.get('alias')

        if not command or not alias:
            return JSONResponse({'success': False}, status=400)

        try:
            result = redis_pool[alias].execute_command(*filter(lambda x: x.strip(), command.split(' ')))
        except ConnectionError, e:
            result = str(e)

        return JSONResponse({'success': True, 'result': result})

    def main_view(self, request, extra_context=None, *args, **kwargs):

        def build_dbs_data():
            for alias, connection in redis_pool.get_connections().iteritems():
                yield {'alias': alias,
                       'status': connection.ping(),
                       'connection': connection,
                       'connection_params': connection.connection_pool.connection_kwargs,
                       'info': connection.info()}

        return render(request, "redis_dashboard/index.html", {'connections': build_dbs_data()})


redis_dashboard_admin = RedisDashboardAdminSite(name="redis_dashboard_admin")
