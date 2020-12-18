from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetView

router = DefaultRouter(trailing_slash=False)
router.register('pets', PetView, basename='pets')

urlpatterns = router.urls
