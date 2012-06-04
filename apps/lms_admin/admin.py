from django.conf import settings

if settings.NONREL:
    from nonreladmin import *
