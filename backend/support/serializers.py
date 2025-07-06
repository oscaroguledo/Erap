from rest_framework import serializers

from crm.models import Customer
from django.contrib.auth.models import User
from .models import Issue, IssueType, MaintenanceVisit, ServiceLevelAgreement, WarrantyClaim, SupportSerialNumber

class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueType
        fields = ['id', 'name', 'description']

class IssueSerializer(serializers.ModelSerializer):
    issue_type = IssueTypeSerializer(read_only=True)
    issue_type_id = serializers.PrimaryKeyRelatedField(
        queryset=IssueType.objects.all(), source='issue_type', write_only=True)
    reported_by = serializers.StringRelatedField(read_only=True)
    assigned_to = serializers.StringRelatedField(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assigned_to', write_only=True, allow_null=True, required=False)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'issue_type', 'issue_type_id', 'reported_by', 'assigned_to', 'assigned_to_id',
            'issue_status', 'priority', 'created_at', 'updated_at', 'first_response_time'
        ]
        read_only_fields = ['created_at', 'updated_at', 'first_response_time']

class SupportMaintenanceVisitSerializer(serializers.ModelSerializer):
    technician = serializers.StringRelatedField(read_only=True)
    technician_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='technician', write_only=True, allow_null=True, required=False)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = MaintenanceVisit
        fields = ['id', 'customer', 'visit_date', 'technician', 'technician_id', 'notes']

class ServiceLevelAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceLevelAgreement
        fields = ['id', 'name', 'description', 'response_time_hours', 'resolution_time_hours', 'active']

class SupportWarrantyClaimSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = WarrantyClaim
        fields = [
            'id', 'customer', 'claim_date', 'product_serial', 'issue_description', 'warrantyclaim_status'
        ]
        read_only_fields = ['claim_date']

class SupportSerialNumberSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)

    class Meta:
        model = SupportSerialNumber
        fields = ['id', 'serial_no', 'product_name', 'warranty_expiry', 'customer']
