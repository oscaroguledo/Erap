from django.db import models
from django.utils import timezone
from crm.models import Customer,SalesPerson
from inventory.models import Item
# Customer and related master data


# Sales Person and Partner

class SalesPartner(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    commission_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

# Item Group and Product Bundle


class ProductBundle(models.Model):
    name = models.CharField(max_length=255, unique=True)
    items = models.ManyToManyField(Item, through='ProductBundleItem')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ProductBundleItem(models.Model):
    product_bundle = models.ForeignKey(ProductBundle, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        unique_together = ('product_bundle', 'item')

# Sales Orders and Quotations

class SalesOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('PARTIALLY_DELIVERED', 'Partially Delivered'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.SET_NULL, null=True, blank=True)
    sales_partner = models.ForeignKey(SalesPartner, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateField(default=timezone.now)
    delivery_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='DRAFT')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.order_number

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=14, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.sales_order.order_number}"

class Quotation(models.Model):
    QUOTATION_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('ORDERED', 'Ordered'),
        ('CANCELLED', 'Cancelled'),
    ]

    quotation_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    sales_person = models.ForeignKey(SalesPerson, on_delete=models.SET_NULL, null=True, blank=True)
    quotation_date = models.DateField(default=timezone.now)
    valid_until = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=QUOTATION_STATUS_CHOICES, default='DRAFT')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.quotation_number

class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=14, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.quotation.quotation_number}"

# Sales Invoice

class SalesInvoice(models.Model):
    INVOICE_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    invoice_number = models.CharField(max_length=100, unique=True)
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=INVOICE_STATUS_CHOICES, default='DRAFT')
    total_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0.0)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invoice_number

class SalesInvoiceItem(models.Model):
    sales_invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=14, decimal_places=2)
    amount = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.sales_invoice.invoice_number}"

# Point of Sale (POS)

class POSProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class POSSettings(models.Model):
    pos_profile = models.OneToOneField(POSProfile, on_delete=models.CASCADE, related_name='settings')
    loyalty_enabled = models.BooleanField(default=False)
    # Add more POS related settings here

    def __str__(self):
        return f"Settings for {self.pos_profile.name}"

class LoyaltyPointEntry(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    points = models.IntegerField()
    entry_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.points} points for {self.customer.name} on {self.entry_date}"
