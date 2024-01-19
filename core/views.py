from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings

def home_view(request):
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
