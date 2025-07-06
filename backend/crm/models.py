from django.db import models
from django.utils import timezone

# Create your models here.
class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    source = models.ForeignKey('LeadSource', on_delete=models.SET_NULL, null=True, blank=True)
    territory = models.ForeignKey('Territory', on_delete=models.SET_NULL, null=True, blank=True)
    lead_status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'), ('Qualified', 'Qualified'), ('Converted', 'Converted'), ('Lost', 'Lost')
    ])
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
class Opportunity(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='opportunities')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)
    opportunity_status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'), ('Won', 'Won'), ('Lost', 'Lost')
    ])
    sales_stage = models.CharField(max_length=50)
    expected_closing = models.DateField()
    expected_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    customer_group = models.ForeignKey('CustomerGroup', on_delete=models.SET_NULL, null=True)
    address = models.TextField(blank=True, null=True)
    territory = models.ForeignKey('Territory', on_delete=models.SET_NULL, null=True)
    contact_person = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Appointment(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    scheduled_time = models.DateTimeField()
    subject = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
class Communication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, choices=[
        ('Call', 'Call'), ('Email', 'Email'), ('Meeting', 'Meeting')
    ])
    notes = models.TextField()
    sender = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
class Territory(models.Model):
    name = models.CharField(max_length=255)

class CustomerGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Prospect(models.Model):
    name = models.CharField(max_length=255)
    source = models.ForeignKey('LeadSource', on_delete=models.SET_NULL, null=True, blank=True)

class SalesPerson(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)

class LeadSource(models.Model):
    name = models.CharField(max_length=255)
class Campaign(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    leads = models.ManyToManyField(Lead, related_name='campaigns')
    notes = models.TextField(blank=True)

class CampaignResult(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    metric = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=2)
class CRMSettings(models.Model):
    default_territory = models.ForeignKey(Territory, on_delete=models.SET_NULL, null=True)
    lead_assignment_rule = models.TextField(blank=True)
    auto_archive_closed_opportunities = models.BooleanField(default=True)
class MaintenanceVisit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    visit_date = models.DateField()
    notes = models.TextField()
    assigned_technician = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True,related_name='crm_maintenance_visits')

class WarrantyClaim(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,related_name='crm_warranty_claims')
    claim_date = models.DateField()
    product_serial = models.CharField(max_length=255)
    issue_description = models.TextField()
    warrantyclaim_status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'), ('In Process', 'In Process'), ('Resolved', 'Resolved'), ('Rejected', 'Rejected')
    ])
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.customer.name})"

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line1}, {self.city}"