from rest_framework import routers
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register('customers', views.CustomerViewSet, basename='customers')
urlpatterns = router.urls
