from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class SiteSettingsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'site'):
            request.site = {
                'name': settings.SCHOOL_NAME
            }


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                raise Http404

        response = self.get_response(request)

        return response
