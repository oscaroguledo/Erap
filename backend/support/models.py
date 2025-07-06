from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from crm.models import Customer  # importing Customer for type hints but not used in ForeignKey string

# Issue and related models
class IssueType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    issue_type = models.ForeignKey(IssueType, on_delete=models.SET_NULL, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    issue_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    priority = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_response_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

# Maintenance Visit model
class MaintenanceVisit(models.Model):
    customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE,related_name='support_maintenance_visits' )  # Corrected to crm.Customer
    visit_date = models.DateField()
    technician = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        
        related_name='support_maintenance_visits'  # unique related_name to avoid clash with crm app
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit for {self.customer} on {self.visit_date}"

# Service Level Agreement (SLA) model
class ServiceLevelAgreement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    response_time_hours = models.PositiveIntegerField(help_text="Max allowed response time in hours")
    resolution_time_hours = models.PositiveIntegerField(help_text="Max allowed resolution time in hours")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Warranty-related models
class WarrantyClaim(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Process', 'In Process'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE,related_name='support_warranty_claims')  # Corrected
    claim_date = models.DateField(default=timezone.now)
    product_serial = models.CharField(max_length=255)
    issue_description = models.TextField()
    warrantyclaim_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')

    def __str__(self):
        return f"Warranty Claim {self.id} for {self.product_serial}"

class SupportSerialNumber(models.Model):
    serial_no = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    warranty_expiry = models.DateField(null=True, blank=True)
    customer = models.ForeignKey('crm.Customer', on_delete=models.SET_NULL, null=True, blank=True)  # Corrected

    def __str__(self):
        return self.serial_no
