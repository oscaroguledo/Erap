from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'opportunities', OpportunityViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'communications', CommunicationViewSet)
router.register(r'territories', TerritoryViewSet)
router.register(r'customer-groups', CustomerGroupViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'prospects', ProspectViewSet)
router.register(r'sales-persons', SalesPersonViewSet)
router.register(r'lead-sources', LeadSourceViewSet)
router.register(r'campaigns', CampaignViewSet)
router.register(r'campaign-results', CampaignResultViewSet)
router.register(r'crm-settings', CRMSettingsViewSet)
router.register(r'maintenance-visits', MaintenanceVisitViewSet)
router.register(r'warranty-claims', WarrantyClaimViewSet)
urlpatterns = [
    path('', include(router.urls)),
    
]
