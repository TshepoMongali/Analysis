from django.db.models import Count, Avg
from .models import Employee
from django.shortcuts import render

# Create your views here.

# people/api.py or people/views.py
from rest_framework import viewsets
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

def dashboard(request):
    gender_stats = Employee.objects.values('gender').annotate(count=Count('id'))
    dept_stats   = Employee.objects.values('department').annotate(count=Count('id'))
    avg_tenure   = Employee.objects.aggregate(avg_years=Avg('tenure_years'))

    return render(request, 'people/dashboard.html',{
        'gender_stats': gender_stats,
        'dept_stats': dept_stats,
        'avg_tenure': avg_tenure,
    })
