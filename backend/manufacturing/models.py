from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True)
    is_raw_material = models.BooleanField(default=False)  # True if raw material, False if finished good

    def __str__(self):
        return self.name

class BillOfMaterials(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='boms')
    description = models.TextField(blank=True, null=True)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"BOM for {self.item.name}"

class BOMComponent(models.Model):
    bom = models.ForeignKey(BillOfMaterials, on_delete=models.CASCADE, related_name='components')
    component = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f"{self.quantity} x {self.component.name} for {self.bom.item.name}"

class WorkstationType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workstation(models.Model):
    name = models.CharField(max_length=255, unique=True)
    workstation_type = models.ForeignKey(WorkstationType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Operation(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    workstation_type = models.ForeignKey(WorkstationType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Routing(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    operations = models.ManyToManyField(Operation, through='RoutingOperation')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Routing for {self.item.name}"

class RoutingOperation(models.Model):
    routing = models.ForeignKey(Routing, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    sequence = models.PositiveIntegerField()

    class Meta:
        unique_together = ('routing', 'operation')
        ordering = ['sequence']

    def __str__(self):
        return f"{self.operation.name} in {self.routing.item.name} (Seq {self.sequence})"

class ProductionPlan(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()
    status_choices = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    productionplan_status = models.CharField(max_length=20, choices=status_choices, default='PLANNED')

    def __str__(self):
        return f"Production Plan for {self.item.name} - Qty: {self.quantity}"

class WorkOrder(models.Model):
    production_plan = models.ForeignKey(ProductionPlan, on_delete=models.CASCADE, related_name='work_orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    scheduled_start_date = models.DateField()
    scheduled_end_date = models.DateField()
    status_choices = [
        ('SCHEDULED', 'Scheduled'),
        ('STARTED', 'Started'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    workorder_status = models.CharField(max_length=20, choices=status_choices, default='SCHEDULED')

    def __str__(self):
        return f"Work Order for {self.item.name} - Qty: {self.quantity}"

class JobCard(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='job_cards')
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    jobcard_status = models.CharField(max_length=20, choices=status_choices, default='PENDING')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Job Card for {self.work_order} - Operation {self.operation.name}"

class DowntimeEntry(models.Model):
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    reason = models.TextField()

    def __str__(self):
        return f"Downtime at {self.workstation.name} from {self.start_time} to {self.end_time}"

class StockEntry(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=3)
    entry_type_choices = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]
    entry_type = models.CharField(max_length=3, choices=entry_type_choices)
    date = models.DateField(auto_now_add=True)
    reference = models.CharField(max_length=255, blank=True, null=True)  # Could link to WorkOrder or JobCard etc.

    def __str__(self):
        return f"{self.entry_type} - {self.quantity} of {self.item.name} on {self.date}"
