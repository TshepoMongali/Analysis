# people/urls.py
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]
# This will automatically create the necessary URL patterns for the EmployeeViewSet.