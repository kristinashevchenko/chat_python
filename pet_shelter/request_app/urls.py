from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PetRequestView

router = DefaultRouter(trailing_slash=False)
router.register('pet_request', PetRequestView, basename='pet_requests')

urlpatterns = router.urls
