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

class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    is_suspicious = models.BooleanField(default=False)
    fraud_flags = models.JSONField(default=dict)  # Store reasons for flagging
    
    class Meta:
        db_table = 'Payments'

class FraudDetector(models.Model):
    """Model for tracking and detecting fraudulent payment patterns"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    last_scan_date = models.DateTimeField(auto_now=True)
    suspicious_pattern_count = models.IntegerField(default=0)
    total_suspicious_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fraud_score = models.FloatField(default=0.0)  # 0 to 1.0, higher means more suspicious
    
    class Meta:
        db_table = 'FraudDetector'
    
    def analyze_payments(self):
        """Analyze payment patterns for this employee"""
        employee_payments = Payment.objects.filter(employee=self.employee).order_by('payment_date')
        
        # Reset analysis
        self.suspicious_pattern_count = 0
        self.total_suspicious_amount = 0
        fraud_indicators = []
        
        if not employee_payments:
            return
        
        # Pattern 1: Unusually large payments
        avg_amount = employee_payments.aggregate(models.Avg('amount'))['amount__avg']
        large_payments = employee_payments.filter(amount__gt=avg_amount * 2)
        if large_payments.exists():
            self.suspicious_pattern_count += 1
            self.total_suspicious_amount += sum(p.amount for p in large_payments)
            fraud_indicators.append("unusually_large_payments")
        
        # Pattern 2: Rapid succession payments
        from datetime import timedelta
        for i in range(len(employee_payments) - 1):
            current = employee_payments[i]
            next_payment = employee_payments[i + 1]
            if (next_payment.payment_date - current.payment_date) < timedelta(days=1):
                current.is_suspicious = True
                current.fraud_flags['rapid_succession'] = True
                next_payment.is_suspicious = True
                next_payment.fraud_flags['rapid_succession'] = True
                current.save()
                next_payment.save()
                self.suspicious_pattern_count += 1
                fraud_indicators.append("rapid_succession_payments")
        
        # Pattern 3: Round number amounts (potential fake invoices)
        round_payments = employee_payments.filter(amount__endswith='.00')
        if round_payments.count() > employee_payments.count() * 0.75:  # If >75% are round numbers
            self.suspicious_pattern_count += 1
            fraud_indicators.append("suspicious_round_amounts")
        
        # Pattern 4: After hours payments
        late_payments = employee_payments.filter(payment_date__hour__gte=18)
        if late_payments.exists():
            self.suspicious_pattern_count += 1
            fraud_indicators.append("after_hours_payments")
        
        # Calculate fraud score (0 to 1)
        max_patterns = 4  # Number of patterns we check
        self.fraud_score = min(self.suspicious_pattern_count / max_patterns, 1.0)
        
        # If fraud score is high, mark employee as potentially fraudulent
        if self.fraud_score > 0.5:
            self.employee.is_fraud = True
            self.employee.save()
        
        self.save()
