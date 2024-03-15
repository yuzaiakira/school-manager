from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from uuid import uuid4

from django.http import Http404


def rename_profile_image(instance, filename):
    new_filename = str(uuid4())
    return 'profile/{}'.format(new_filename)


# TODO: try to delete this func 
def editable(request):
    return request.user.can_edit or request.user.group.can_edit


def check_is_admin(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url='admin:login'):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)

    raise Http404
