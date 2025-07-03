from django.db import models


# Create your models here.
class Employee(models.Model):
    
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    WORK_LOCATIONS = [('Remote', 'Remote'), ('On-site', 'On-site'), ('Hybrid', 'Hybrid')]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()
    hire_date = models.DateField()
    work_location = models.CharField(max_length=10, choices=WORK_LOCATIONS, default ='Remote')
    # add fields like satisfaction_level, salary, turnover_flag etc.
class LeaveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    
