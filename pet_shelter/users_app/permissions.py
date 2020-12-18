from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


def _is_superuser_user(user):
    superuser = User.objects.filter(is_superuser=True, username=user)
    return True if superuser else False


class IsSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.user and request.user.is_authenticated \
                and _is_superuser_user(request.user):
            return True

        return False
