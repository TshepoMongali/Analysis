# people/urls.py
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet
from django.urls import path
from . import views
from .views import index_view

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = router.urls


urlpatterns = [
    path('dashboard/<int:employee_id>/', views.dashboard, name='dashboard'),
    path('index/', index_view, name='index'),
]
# This will automatically create the necessary URL patterns for the EmployeeViewSet.