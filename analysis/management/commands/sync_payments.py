from django.core.management.base import BaseCommand
from analysis.db_config import fetch_payments
from analysis.models import Employee, Payment
from datetime import datetime

class Command(BaseCommand):
    help = 'Sync payments from Access database'

    def handle(self, *args, **kwargs):
        payments = fetch_payments()
        count = 0
        
        for payment_data in payments:
            try:
                # Assuming payment_data has employee_id to link with Employee
                employee = Employee.objects.get(id=payment_data['employee_id'])
                
                # Convert date string to datetime if needed
                payment_date = payment_data['payment_date']
                if isinstance(payment_date, str):
                    payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
                
                # Create or update payment record
                Payment.objects.update_or_create(
                    reference=payment_data['reference'],  # Use as unique identifier
                    defaults={
                        'employee': employee,
                        'payment_date': payment_date,
                        'amount': payment_data['amount'],
                        'payment_type': payment_data['payment_type'],
                        'status': payment_data['status'],
                    }
                )
                count += 1
            except Employee.DoesNotExist:
                self.stderr.write(f"Employee not found for payment {payment_data['reference']}")
            except Exception as e:
                self.stderr.write(f"Error processing payment: {str(e)}")
        
        self.stdout.write(self.style.SUCCESS(f'Successfully synced {count} payments'))