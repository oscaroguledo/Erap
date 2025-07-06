# models/setup.py
from django.db import models
from accounting.models import Company

class Branch(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Designation(models.Model):
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

class EmployeeGrade(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

# models/employee.py
class Employee(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('CN', 'Contract'),
        ('IN', 'Intern'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('resigned', 'Resigned'),
        ('terminated', 'Terminated'),
    ]

    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_joining = models.DateField()
    date_of_birth = models.DateField()
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPE_CHOICES)
    employee_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    grade = models.ForeignKey(EmployeeGrade, on_delete=models.SET_NULL, null=True)

# models/leave.py
class LeaveType(models.Model):
    name = models.CharField(max_length=255)
    max_leaves = models.DecimalField(max_digits=5, decimal_places=2)
    carry_forward = models.BooleanField(default=False)

class LeaveAllocation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    total_leaves = models.DecimalField(max_digits=5, decimal_places=2)
    from_date = models.DateField()
    to_date = models.DateField()

class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    leave_application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)

# models/attendance.py
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('on_leave', 'On Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    attendance_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.TextField(blank=True)

class EmployeeCheckin(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    log_type = models.CharField(max_length=10, choices=[('in', 'IN'), ('out', 'OUT')])

# models/expense.py
class EmployeeAdvance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.TextField()
    date = models.DateField()

class ExpenseClaim(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    advance = models.ForeignKey(EmployeeAdvance, on_delete=models.SET_NULL, null=True, blank=True)
    expense_date = models.DateField()
    purpose = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_claim_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

# models/hr_settings.py
class HRSettings(models.Model):
    default_working_hours = models.PositiveIntegerField(default=8)
    attendance_required = models.BooleanField(default=True)
    leave_auto_approval = models.BooleanField(default=False)
