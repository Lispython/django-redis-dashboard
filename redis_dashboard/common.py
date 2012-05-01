#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
redis_dashboard.common
~~~~~~~~~~~~~~~~~~~~~~

Core functions to store redis connections

:copyright: (c) 2012 by Alexandr Sokolovskiy (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""


from django.conf import settings

from redis import Redis


class ConnectionError(Exception):
    """Redis connection error"""


class ConnectionsPool(object):

    def __init__(self):
        self.REDIS_DBS = getattr(settings, 'REDIS_DBS', None)
        self.__connections = {}

    def __getitem__(self, name):

        # Get redis connections settings from config
        if not self.REDIS_DBS:
            raise ConnectionError("Can't find settings for redis connection")

        if name not in self.__connections:
            connection_settings = self.REDIS_DBS.get(name)

            if not connection_settings:
                raise ConnectionError("Can't find settings for alias %" % name)
            else:
                self.__connections[name] = self.create_connection(connection_settings)
        return self.__connections[name]

    def create_connection(self, alias_settings):
        """Create redis connection for given alias settings"""
        return Redis(
            host=alias_settings.get("HOST", '127.0.0.1'),
            port=alias_settings.get("PORT", 6379),
            db=alias_settings.get("DB", 1),
            password=alias_settings.get("PASSWORD"))

    def get_connections(self):
        for alias, config in self.REDIS_DBS.iteritems():
            try:
                if alias not in self.__connections.keys():
                    self.__connections[alias] = self.create_connection(config)
            except Exception, e:
                print(e)
        return self.__connections

    def __len__(self):
        return len(self.__connections)

    @property
    def len_dbs(self):
        return len(settings.REDIS_DBS)


# Create pool instance and default redis connection
redis_pool = ConnectionsPool()
default_redis = redis_pool['default']
