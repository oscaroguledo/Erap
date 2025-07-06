from django.db import models
from django.utils import timezone

# 1. Item and related master data

class ItemGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.abbreviation

class Item(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    item_group = models.ForeignKey(ItemGroup, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    reorder_level = models.DecimalField(max_digits=12, decimal_places=3, default=0)  # for stock alerts
    # Additional fields: variants, serial numbers, batch etc can be added later

    def __str__(self):
        return f"{self.sku} - {self.name}"

# 2. Warehouse Setup

class Warehouse(models.Model):
    code = models.CharField(max_length=50, unique=True)  # e.g. GH, WIP01
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

# 3. Stock Ledger Entry (transaction log)

class StockLedgerEntry(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('TRANSFER', 'Transfer'),
        ('ADJUSTMENT', 'Adjustment'),
    ]

    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    transaction_date = models.DateTimeField(default=timezone.now)
    reference_doc = models.CharField(max_length=255, blank=True, null=True)  # e.g. Purchase Order #, Delivery Note #
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} {self.item} @ {self.warehouse} on {self.transaction_date}"

# 4. Stock Entry (main document recording stock movement)

class StockEntry(models.Model):
    ENTRY_TYPES = [
        ('RECEIPT', 'Goods Receipt'),
        ('ISSUE', 'Goods Issue'),
        ('TRANSFER', 'Stock Transfer'),
        ('REPACK', 'Repackaging'),
        ('ADJUSTMENT', 'Stock Adjustment'),
    ]

    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    posting_date = models.DateField(default=timezone.now)
    posting_time = models.TimeField(default=timezone.now)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='stockentry_from')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='stockentry_to')
    reference_doc = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type} on {self.posting_date} ref: {self.reference_doc or 'N/A'}"


# 5. Stock Balance (denormalized for quick lookups)

class StockBalance(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    class Meta:
        unique_together = ('item', 'warehouse')

    def __str__(self):
        return f"{self.item} - {self.quantity} @ {self.warehouse}"

# 6. Stock Opening Balance (initial stock setting)

class StockOpeningBalance(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    posting_date = models.DateField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('item', 'warehouse')

    def __str__(self):
        return f"Opening {self.quantity} {self.item} @ {self.warehouse} on {self.posting_date}"
class Batch(models.Model):
    batch_number = models.CharField(max_length=100, unique=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    manufacture_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Batch {self.batch_number} - {self.item.name}"

class InventorySerialNumber(models.Model):
    serial_number = models.CharField(max_length=100, unique=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='serial_numbers')
    status_choices = [
        ('AVAILABLE', 'Available'),
        ('SOLD', 'Sold'),
        ('DAMAGED', 'Damaged'),
        ('RETURNED', 'Returned'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='AVAILABLE')
    warranty_expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"SN {self.serial_number} - {self.item.name}"

class StockEntryItem(models.Model):
    stock_entry = models.ForeignKey('StockEntry', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('Item', on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    uom = models.ForeignKey('UnitOfMeasure', on_delete=models.PROTECT)

    # New fields linking Batch and Serial Numbers
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    serial_numbers = models.ManyToManyField(InventorySerialNumber, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.item} in {self.stock_entry}"

    def clean(self):
        # Optionally add validation: If serial_numbers are provided,
        # quantity must equal the number of serial_numbers
        if self.serial_numbers.exists() and self.quantity != self.serial_numbers.count():
            from django.core.exceptions import ValidationError
            raise ValidationError("Quantity must match the number of serial numbers assigned.")
        