from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# -- Project Structure & Setup --

class ProjectType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.CharField(max_length=255, blank=True)
    project_status = models.CharField(max_length=50, choices=[
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled')
    ], default='Open')
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# -- Project Planning --

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.project.name}"


# -- Task Management --

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    task_status = models.CharField(max_length=50, choices=[
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Overdue', 'Overdue'),
        ('Completed', 'Completed')
    ], default='Not Started')

    def __str__(self):
        return self.title


class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    update_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


# -- Time Tracking --

class ActivityType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ActivityCost(models.Model):
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.activity_type.name} - {self.cost_per_hour}/hr"


class Timesheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    work_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.hours} hrs"


# -- Project Billing & Costing --

class ProjectExpense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount} on {self.date}"


class ProjectInvoice(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=100)
    billed_to = models.CharField(max_length=255)
    issue_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.invoice_number} - {self.project.name}"
