from django.db import models

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=[('M','Male'),('F','Female')])
    age = models.IntegerField()
    hire_date = models.DateField()
    # add fields like satisfaction_level, salary, turnover_flag etc.
