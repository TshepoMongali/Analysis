import os
import sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','Best.settings')
import django
django.setup()
from analysis.models import Employee
emp = Employee.objects.create(first_name='Tshepo', last_name='Fake', department='Fraud', gender='M', age=35, hire_date='2021-06-01', work_location='On-site')
print('Created', emp.id, emp.first_name, 'is_fraud=', emp.is_fraud)
