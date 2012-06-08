from django.conf.urls.defaults import *
from alerts.views import AlertList, acknowledge
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('zimbra.views',
                       url('^preauth/$', 'preauth', name = 'preauth'),
                       )
