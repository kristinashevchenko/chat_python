from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Pet
from .serializers import PetSerializer


class PetView(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
