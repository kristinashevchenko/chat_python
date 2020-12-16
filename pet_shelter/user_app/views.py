from django.shortcuts import render
from rest_framework import viewsets, permissions, response, status, exceptions
from rest_framework.decorators import action
from .serializers import LoginCustomerSerializer, CustomerSerializer
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your views here.
class CustomerViewSet(viewsets.GenericViewSet, APIView):

    queryset = User.objects.filter(is_active=True, is_superuser=False, is_customer=True)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CustomerSerializer

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='login',
    )
    def login(self, request, *args, **kwargs):
        serializer = LoginCustomerSerializer(data=request.data)
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

    def _register_temp_user(self, request):
        temp_user = User.objects.create_temp_user()
        serializer = self.get_serializer(temp_user)

        return response.Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def _register_after_skip(self, request):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_temporary=False)

        return response.Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def _register_user(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_temporary=False)

        return response.Response(status=status.HTTP_201_CREATED, data=serializer.data)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='register',
    )
    def register(self, request, *args, **kwargs):
        '''There is only 3 cases to register:
           1) create temporary user - register using skip registration
           2) update temporary to permanent user - register after skip
           3) create permanent user without skip
        '''
        skip_registration = request.data.get('skip_registration', False)
        print(request.user, request.user.is_authenticated, skip_registration)

        if skip_registration and request.user and not request.user.is_authenticated:
            return self._register_temp_user(request, *args, **kwargs)
        elif request.user and request.user.is_authenticated and request.user.is_temporary:
            return self._register_after_skip(request, *args, **kwargs)
        elif request.user and not request.user.is_authenticated:
            return self._register_user(request, *args, **kwargs)
        else:
            raise exceptions.PermissionDenied()
