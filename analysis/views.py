from django.db.models import Count, Avg, F
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
# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
# The API URLs are now determined automatically by the router.
urlpatterns = router.urls
# Add the dashboard URL
urlpatterns += [
    path('dashboard/', dashboard, name='dashboard'),
]




def dashboard_view(request):
    today = date.today()

    gender_stats = Employee.objects.values('gender').annotate(count=Count('id'))
    department_stats = Employee.objects.values('department').annotate(count=Count('id'))
    job_roles = Employee.objects.values('role').annotate(count=Count('id'))
    work_location_data = Employee.objects.values('work_location').annotate(count=Count('id'))

    # Age Ranges
    age_data = [
        {'range': '20-29', 'count': Employee.objects.filter(age__gte=20, age__lte=29).count()},
        {'range': '30-39', 'count': Employee.objects.filter(age__gte=30, age__lte=39).count()},
        {'range': '40-49', 'count': Employee.objects.filter(age__gte=40, age__lte=49).count()},
        {'range': '50+', 'count': Employee.objects.filter(age__gte=50).count()}
    ]

    # Tenure
    tenure_data = [
        {'range': '0-1 years', 'count': Employee.objects.filter(hire_date__gte=today.replace(year=today.year - 1)).count()},
        {'range': '1-3 years', 'count': Employee.objects.filter(hire_date__lt=today.replace(year=today.year - 1), hire_date__gte=today.replace(year=today.year - 3)).count()},
        {'range': '3-5 years', 'count': Employee.objects.filter(hire_date__lt=today.replace(year=today.year - 3), hire_date__gte=today.replace(year=today.year - 5)).count()},
        {'range': '5+ years', 'count': Employee.objects.filter(hire_date__lt=today.replace(year=today.year - 5)).count()}
    ]

    # Leave types
    

    context = {
        'gender_stats': list(gender_stats),
        'department_stats': list(department_stats),
        'job_roles': list(job_roles),
        'work_location_data': list(work_location_data),
        
        'tenure_data': tenure_data,
        'age_data': age_data,
        'satisfaction_data': [
            {'month': 'Jan', 'score': 7.5},
            {'month': 'Feb', 'score': 8.1},
            {'month': 'Mar', 'score': 7.9},
            {'month': 'Apr', 'score': 8.2},
            {'month': 'May', 'score': 7.7}
        ]
    }
    return render(request, 'dashboard.html', context)
