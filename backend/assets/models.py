from django.db import models
from django.utils import timezone

class AssetCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    # Depreciation settings
    DEPRECIATION_METHOD_CHOICES = [
        ('STRAIGHT_LINE', 'Straight Line'),
        ('DECLINING_BALANCE', 'Declining Balance'),
        ('SUM_OF_YEARS_DIGITS', 'Sum of Years Digits'),
        ('UNITS_OF_PRODUCTION', 'Units of Production'),
    ]
    depreciation_method = models.CharField(max_length=50, choices=DEPRECIATION_METHOD_CHOICES, default='STRAIGHT_LINE')
    depreciation_duration_months = models.PositiveIntegerField(default=60)  # e.g. 5 years
    fixed_asset_account = models.CharField(max_length=255, blank=True, null=True)  # Could link to accounting chart later
    depreciation_account = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class AssetLocation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Asset(models.Model):
    asset_tag = models.CharField(max_length=100, unique=True)  # Unique identifier like a serial or tag number
    name = models.CharField(max_length=255)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT, related_name='assets')
    location = models.ForeignKey(AssetLocation, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    salvage_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    useful_life_months = models.PositiveIntegerField(default=60)  # in months
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class AssetDepreciation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='depreciations')
    depreciation_date = models.DateField(default=timezone.now)
    depreciation_amount = models.DecimalField(max_digits=14, decimal_places=2)
    accumulated_depreciation = models.DecimalField(max_digits=14, decimal_places=2)
    net_book_value = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"Depreciation for {self.asset} on {self.depreciation_date}"


class AssetMaintenanceTeam(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AssetMaintenance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenances')
    maintenance_team = models.ForeignKey(AssetMaintenanceTeam, on_delete=models.SET_NULL, null=True, blank=True)
    maintenance_date = models.DateField(default=timezone.now)
    description = models.TextField()
    cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    next_due_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Maintenance for {self.asset} on {self.maintenance_date}"


class AssetMaintenanceLog(models.Model):
    maintenance = models.ForeignKey(AssetMaintenance, on_delete=models.CASCADE, related_name='logs')
    log_date = models.DateTimeField(default=timezone.now)
    description = models.TextField()

    def __str__(self):
        return f"Log for {self.maintenance} at {self.log_date}"


class AssetValueAdjustment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='value_adjustments')
    adjustment_date = models.DateField(default=timezone.now)
    adjustment_amount = models.DecimalField(max_digits=14, decimal_places=2)  # Positive or negative
    reason = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Value Adjustment for {self.asset} on {self.adjustment_date}"
