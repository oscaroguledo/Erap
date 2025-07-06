from rest_framework import serializers
from .models import (
    ProjectType, Project, Milestone, Task, ProjectUpdate,
    ActivityType, ActivityCost, Timesheet,
    ProjectExpense, ProjectInvoice
)

class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUpdate
        fields = '__all__'

class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = '__all__'

class ActivityCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCost
        fields = '__all__'

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = '__all__'

class ProjectExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectExpense
        fields = '__all__'

class ProjectInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectInvoice
        fields = '__all__'
