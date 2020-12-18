from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status, exceptions, mixins
from rest_framework.decorators import action
from .serializers import LoginSerializer, CustomerSerializer, VolunteerSerializer, SuperuserSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .permissions import IsSuperuser


User = get_user_model()


def _is_superuser_user(user):
    superuser = User.objects.filter(is_superuser=True, username=user)
    return True if superuser else False


class MeAbstractApiView:
    @action(
        methods=['get', 'put', 'patch'],
        detail=False,
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(request.user)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)


class LoginLogoutApiView:
    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='login',
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return response.Response(status=status.HTTP_200_OK, data=dict(token=serializer.extract_token()))

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='logout',
    )
    def logout(self, request, *args, **kwargs):
        user = request.user
        user.auth_token.delete()

        return response.Response(status=status.HTTP_200_OK)


# Create your views here.
class CustomerViewSet(viewsets.GenericViewSet, APIView, MeAbstractApiView, LoginLogoutApiView):

    queryset = User.objects.filter(is_active=True, is_superuser=False, is_volunteer=False, is_customer=True)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CustomerSerializer

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='register',
    )
    def register(self, request, *args, **kwargs):
        if request.user and not request.user.is_authenticated:
            return self._register_user(request, *args, **kwargs)
        else:
            raise exceptions.PermissionDenied()

    def _register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_customer = request.data.get('is_customer', False)
        serializer.save(is_customer=is_customer)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class VolunteerViewSet(viewsets.ModelViewSet, APIView, LoginLogoutApiView, MeAbstractApiView):

    queryset = User.objects.filter(is_active=True, is_superuser=False, is_volunteer=True, is_customer=False)
    permission_classes = [permissions.IsAuthenticated, IsSuperuser, ]
    serializer_class = VolunteerSerializer

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='register',
    )
    def register(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated\
                and _is_superuser_user(request.user):
            return self._register_user(request, *args, **kwargs)
        else:
            raise exceptions.PermissionDenied()

    def _register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_volunteer = request.data.get('is_volunteer', True)
        serializer.save(is_volunteer=is_volunteer)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SuperuserViewSet(viewsets.GenericViewSet, APIView, LoginLogoutApiView):

    queryset = User.objects.filter(is_active=True, is_superuser=True, is_volunteer=False, is_customer=False)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = SuperuserSerializer

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='register',
    )
    def register(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated\
                and _is_superuser_user(request.user):
            return self._register_user(request, *args, **kwargs)
        else:
            raise exceptions.PermissionDenied()

    def _register_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_superuser = request.data.get('is_superuser', True)
        serializer.save(is_superuser=is_superuser)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
