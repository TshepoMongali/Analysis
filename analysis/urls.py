# people/urls.py
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = router.urls
# This will automatically create the necessary URL patterns for the EmployeeViewSet.