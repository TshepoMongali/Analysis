from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/<int:employee_id>/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('employee/add/', views.add_employee, name='add_employee'),
]