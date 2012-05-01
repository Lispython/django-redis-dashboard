#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
redis_dashboard
~~~~~~~~~~~~~~~

Application to show redis servers statistics in django admin interface

:copyright: (c) 2012 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
"""

__all__ = ('get_version', )
__author__ = "Alex Lispython (alex@obout.ru)"
__license__ = "BSD, see LICENSE for more details"
__version_info__ = (0, 0, 1)
__version__ = ".".join(map(str, __version_info__))
__maintainer__ = "Alexandr Lispython (alex@obout.ru)"


def get_version():
    return __version__
