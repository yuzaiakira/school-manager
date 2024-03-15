from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class UserLoginRequiredMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL


class UserAuthorizationMixin(UserLoginRequiredMixin, PermissionRequiredMixin):
    redirect_field_name = settings.REDIRECT_FIELD_NAME
