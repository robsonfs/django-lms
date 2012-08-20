from time import time
import hmac, hashlib

from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from libs.django_utils import render_to_response

@login_required
def preauth(request):
    timestamp = int(time()*1000)

    #If they're not logged in, an exception will be thrown.
    acct = request.user.email
    
    pak = hmac.new(settings.ZIMBRA_PREAUTH, '%s|name|0|%s'%(acct, timestamp), hashlib.sha1).hexdigest()
    return HttpResponseRedirect("//%s/service/preauth?account=%s&expires=0&timestamp=%s&preauth=%s"%(settings.ZIMBRA_URL, acct, timestamp, pak))

