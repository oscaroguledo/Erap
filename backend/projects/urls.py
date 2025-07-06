from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectTypeViewSet, ProjectViewSet, MilestoneViewSet, TaskViewSet, ProjectUpdateViewSet,
    ActivityTypeViewSet, ActivityCostViewSet, TimesheetViewSet,
    ProjectExpenseViewSet, ProjectInvoiceViewSet
)

router = DefaultRouter()
router.register(r'project-types', ProjectTypeViewSet, basename='projecttype')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'milestones', MilestoneViewSet, basename='milestone')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'project-updates', ProjectUpdateViewSet, basename='projectupdate')
router.register(r'activity-types', ActivityTypeViewSet, basename='activitytype')
router.register(r'activity-costs', ActivityCostViewSet, basename='activitycost')
router.register(r'timesheets', TimesheetViewSet, basename='timesheet')
router.register(r'project-expenses', ProjectExpenseViewSet, basename='projectexpense')
router.register(r'project-invoices', ProjectInvoiceViewSet, basename='projectinvoice')

urlpatterns = [
    path('', include(router.urls)),
    
]
