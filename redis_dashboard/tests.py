#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from redis_dashboard.common import redis_pool, default_redis

class DashboardTestCase(TestCase):

    def setUp(self):
        admin = User.objects.create_superuser("test_user", "test_email@example.com", "password")
        admin.save()
        self.admin = admin

    def test_index(self):
        client = Client()
        client.login(username=self.admin.username, password='password')
        response = client.get(reverse("redis_dashboard_admin:index"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Redis DBS connections")
        self.assertContains(response, "127.0.0.1:6479[1]")
        self.assertContains(response, "127.0.0.1:6479[2]")
        ## self.assertEquals(len([x for x in response.context['connections']]), len(settings.REDIS_DBS))

    def test_details(self):
        client = Client()
        client.login(username=self.admin.username, password='password')
        response = client.get(reverse("redis_dashboard_admin:details", kwargs={'alias': 'default'}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Command line interface")
        self.assertEquals(response.context['alias'], 'default')

    def test_connections_pool(self):
        self.assertEquals(len(settings.REDIS_DBS), redis_pool.len_dbs)

        for key, value in settings.REDIS_DBS['default'].iteritems():
            self.assertEquals(settings.REDIS_DBS['default'][key],
                              default_redis.connection_pool.connection_kwargs[key.lower()])
        self.assertEquals(len(settings.REDIS_DBS), len(redis_pool.get_connections()))

    def test_execute_command(self):
        client = Client()
        client.login(username=self.admin.username, password='password')

        bad_response = client.post(reverse("redis_dashboard_admin:execute-command"),
                                   {'command': 'info'})
        self.assertEquals(bad_response.status_code, 400)

        response = client.post(reverse("redis_dashboard_admin:execute-command"),
                               {'command': 'INFO',
                                'alias': 'default'})

        response = client.post(reverse("redis_dashboard_admin:execute-command"),
                               {'command': 'keys * ',
                                'alias': 'default'})
        print(response)

        self.assertEquals(response.status_code, 200)
