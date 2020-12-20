from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetView, AnimalView

router = DefaultRouter(trailing_slash=False)
router.register('pets', PetView, basename='pets')
router.register('animals', AnimalView, basename='animals')

urlpatterns = router.urls
