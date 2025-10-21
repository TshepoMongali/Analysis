from datetime import date
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import Employee


def index(request):
    employees = Employee.objects.all()
    return render(request, 'index.html', {'employees': employees})


def dashboard(request, employee_id=None):
    # if employee_id provided, show details, else show summary dashboard
    if employee_id:
        employee = get_object_or_404(Employee, id=employee_id)
        return render(request, 'dashboard.html', {'employee': employee})

    employees = Employee.objects.all()
    # gender counts
    male = employees.filter(gender='M').count()
    female = employees.filter(gender='F').count()
    gender_stats = json.dumps({'M': male, 'F': female})

    # average tenure (years)
    today = date.today()
    if employees.exists():
        total_tenure = sum((today.year - e.hire_date.year) for e in employees)
        avg_tenure = total_tenure / employees.count()
    else:
        avg_tenure = 0

    return render(request, 'dashboard.html', {
        'gender_stats': gender_stats,
        'avg_tenure': round(avg_tenure, 2)
    })


@require_http_methods(["GET", "POST"])
def add_employee(request):
    """A simple view to add an Employee via an HTML form.

    GET: render a form
    POST: validate input and create Employee, then redirect to index
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        department = request.POST.get('department', '').strip()
        gender = request.POST.get('gender', '').strip()
        age = request.POST.get('age', '').strip()
        salary = request.POST.get('salary', '').strip()
        hire_date = request.POST.get('hire_date', '').strip()
        work_location = request.POST.get('work_location', '').strip() or 'Remote'

        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if gender not in ('M', 'F'):
            errors.append('Gender must be M or F.')
        try:
            age = int(age)
            if age <= 0:
                errors.append('Age must be a positive integer.')
        except Exception:
            errors.append('Age must be an integer.')

        try:
            # salary optional, default 0.00
            salary = float(salary) if salary else 0.00
        except Exception:
            errors.append('Salary must be a number.')

        # Basic date validation (YYYY-MM-DD)
        try:
            parts = [int(p) for p in hire_date.split('-')]
            if len(parts) != 3:
                raise ValueError()
        except Exception:
            errors.append('Hire date must be in YYYY-MM-DD format.')

        if errors:
            return render(request, 'add_employee.html', {'errors': errors, 'form': request.POST})

        # Create employee. Model.save() will enforce fraud/last_name if applicable.
        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            department=department,
            gender=gender,
            age=age,
            salary=salary,
            hire_date=hire_date,
            work_location=work_location,
        )

        return redirect('index')

    return render(request, 'add_employee.html')
