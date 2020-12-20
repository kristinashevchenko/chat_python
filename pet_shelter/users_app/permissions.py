from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


def _is_superuser_user(user):
    superuser = User.objects.filter(is_superuser=True, username=user)
    return True if superuser else False


def _is_customer_user(user):
    customer = User.objects.filter(is_customer=True, username=user)
    return True if customer else False


def _is_volunteer_user(user):
    volunteer = User.objects.filter(is_volunteer=True, username=user)
    return True if volunteer else False


class IsSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow superuser to have access to objects.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated \
                and _is_superuser_user(request.user):
            return True

        return False


class IsVolunteer(permissions.BasePermission):
    """
    Custom permission to only allow volunteer to have access to objects.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated \
                and _is_volunteer_user(request.user):
            return True

        return False


class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customer to have access to objects.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated \
                and _is_customer_user(request.user):
            return True

        return False

