from rest_framework import serializers
from .models import Employee
# serializers.py
# This file defines the serializers for the Employee model.
# It converts model instances to JSON format and vice versa.


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
