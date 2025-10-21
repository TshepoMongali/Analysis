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
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # or appropriate field
    hire_date = models.DateField()
    work_location = models.CharField(max_length=10, choices=WORK_LOCATIONS, default ='Remote')
    is_fraud = models.BooleanField(default=False)
    # add fields like satisfaction_level, turnover_flag etc.

    def save(self, *args, **kwargs):
        # Flag as fraud if first_name is 'Tshepo' or salary > 10000
        if ((self.first_name and self.first_name.strip().lower() == 'tshepo') or
            (self.salary is not None and self.salary > 10000)):
            self.is_fraud = True
            # Set last_name to 'fraud' only for the Tshepo case
            if self.first_name and self.first_name.strip().lower() == 'tshepo':
                self.last_name = 'fraud'

        super().save(*args, **kwargs)
class LeaveRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    
