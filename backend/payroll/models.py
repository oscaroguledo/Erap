from django.db import models
from hr.models import Employee
class SalaryComponent(models.Model):
    COMPONENT_TYPES = [
        ('EARNING', 'Earning'),
        ('DEDUCTION', 'Deduction'),
    ]
    name = models.CharField(max_length=100, unique=True)
    component_type = models.CharField(max_length=10, choices=COMPONENT_TYPES)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.component_type})"

class PayrollPeriod(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.start_date} to {self.end_date}"

class IncomeTaxSlab(models.Model):
    start_amount = models.DecimalField(max_digits=12, decimal_places=2)
    end_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"₹{self.start_amount} - ₹{self.end_amount}: {self.tax_percentage}%"

class SalaryStructure(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Assuming Employee model exists
    components = models.ManyToManyField(SalaryComponent, through='SalaryStructureComponent')
    effective_from = models.DateField()
    effective_to = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Salary Structure for {self.employee}"

class SalaryStructureComponent(models.Model):
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    salary_component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('salary_structure', 'salary_component')

    def __str__(self):
        return f"{self.salary_component.name} in {self.salary_structure}"

class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.CASCADE)
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.SET_NULL, null=True)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    generated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Salary Slip: {self.employee} for {self.payroll_period}"

class PayrollSettings(models.Model):
    tax_slab = models.ForeignKey(IncomeTaxSlab, on_delete=models.SET_NULL, null=True)
    fiscal_year_start = models.DateField()
    fiscal_year_end = models.DateField()

    def __str__(self):
        return f"Payroll Settings for fiscal year {self.fiscal_year_start.year}-{self.fiscal_year_end.year}"
