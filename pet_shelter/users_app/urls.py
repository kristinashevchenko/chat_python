from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('volunteers', views.VolunteerViewSet, basename='volunteers')
router.register('superusers', views.SuperuserViewSet, basename='superusers')
urlpatterns = router.urls
