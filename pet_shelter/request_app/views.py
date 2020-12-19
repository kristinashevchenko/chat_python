from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from .models import PetRequest, closedStatus, nonAppearanceStatus
from .serializers import PetSerializer
from .permissions import IsCustomer, IsVolunteer
from django.contrib.auth import get_user_model

User = get_user_model()


class PetRequestView(viewsets.ModelViewSet):
    queryset = PetRequest.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsCustomer, ]
        else:
            permission_classes = [IsVolunteer, ]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.user).first()
        request.data['user'] = user.id

        return super(PetRequestView, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        status = request.data['status']
        if status and (status == closedStatus or status == nonAppearanceStatus):
            return super(PetRequestView, self).destroy(request, *args, **kwargs)

        raise exceptions.ValidationError('Invalid status request')
