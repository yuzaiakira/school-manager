from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserAuthorizationMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.REDIRECT_FIELD_NAME