from django.core.management.base import BaseCommand
from django.db import transaction
from analysis.models import Employee, Payment, FraudDetector
from analysis.db_config import fetch_payments
from datetime import datetime

class Command(BaseCommand):
    help = 'Analyze payments for fraud patterns'

    def add_arguments(self, parser):
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Analyze specific employee only',
        )

    def handle(self, *args, **options):
        # First sync payments from Access
        self.stdout.write('Syncing payments from Access database...')
        payments = fetch_payments()
        
        with transaction.atomic():
            # Create/update payments
            for payment_data in payments:
                try:
                    employee = Employee.objects.get(id=payment_data['employee_id'])
                    payment_date = payment_data['payment_date']
                    if isinstance(payment_date, str):
                        payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
                    
                    Payment.objects.update_or_create(
                        reference=payment_data['reference'],
                        defaults={
                            'employee': employee,
                            'payment_date': payment_date,
                            'amount': payment_data['amount'],
                            'payment_type': payment_data['payment_type'],
                            'status': payment_data['status'],
                            'is_suspicious': False,
                            'fraud_flags': {},
                        }
                    )
                except Employee.DoesNotExist:
                    self.stderr.write(f"Employee not found for payment {payment_data['reference']}")
                except Exception as e:
                    self.stderr.write(f"Error processing payment: {str(e)}")
        
        # Run fraud detection
        self.stdout.write('Running fraud detection analysis...')
        
        employees = Employee.objects.all()
        if options['employee_id']:
            employees = employees.filter(id=options['employee_id'])
        
        for employee in employees:
            detector, _ = FraudDetector.objects.get_or_create(employee=employee)
            try:
                detector.analyze_payments()
                self.stdout.write(f"Analyzed employee {employee.id}: fraud score {detector.fraud_score:.2f}")
                
                if detector.fraud_score > 0.5:
                    self.stdout.write(
                        self.style.WARNING(
                            f"⚠️ High fraud score for {employee.first_name} {employee.last_name}: "
                            f"{detector.fraud_score:.2f} "
                            f"({detector.suspicious_pattern_count} suspicious patterns, "
                            f"${detector.total_suspicious_amount:.2f} suspicious amount)"
                        )
                    )
            except Exception as e:
                self.stderr.write(f"Error analyzing employee {employee.id}: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS('Fraud detection complete'))