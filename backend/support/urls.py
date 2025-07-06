from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IssueTypeViewSet, IssueViewSet, MaintenanceVisitViewSet,
    ServiceLevelAgreementViewSet, WarrantyClaimViewSet, SupportSerialNumberViewSet
)

router = DefaultRouter()
router.register(r'issue-types', IssueTypeViewSet, basename='issue-type')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'maintenance-visits', MaintenanceVisitViewSet, basename='maintenance-visit')
router.register(r'service-level-agreements', ServiceLevelAgreementViewSet, basename='service-level-agreement')
router.register(r'warranty-claims', WarrantyClaimViewSet, basename='warranty-claim')
router.register(r'serial-numbers', SupportSerialNumberViewSet, basename='serial-number')

urlpatterns = [
    path('', include(router.urls)),
]
