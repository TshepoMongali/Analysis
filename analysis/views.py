from django.db.models import Count, Avg
from .models import Employee
from django.shortcuts import render
from datetime import date
import json
from .serializers import EmployeeSerializer
from rest_framework import serializers
from django.urls import path
from rest_framework.routers import DefaultRouter
# analysis/views.py



# Create your views here.

# people/api.py or people/views.py
from rest_framework import viewsets
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

def dashboard(request):
    employees = Employee.objects.all()

    # Calculate gender stats
    male = employees.filter(gender='Male').count()
    female = employees.filter(gender='Female').count()
    gender_stats = json.dumps({'Male': male, 'Female': female})

    # Calculate tenure stats manually
    today = date.today()
    total_tenure = 0
    for emp in employees:
        tenure = today.year - emp.hire_date.year
        total_tenure += tenure

    avg_tenure = total_tenure / employees.count() if employees.exists() else 0

    return render(request, 'dashboard.html', {
        'gender_stats': gender_stats,
        'avg_tenure': round(avg_tenure, 2),
    })