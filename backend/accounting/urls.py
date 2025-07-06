from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'fiscalyears', FiscalYearViewSet)
router.register(r'paymentterms', PaymentTermViewSet)
router.register(r'paymentmodes', PaymentModeViewSet)
router.register(r'taxcategories', TaxCategoryViewSet)
router.register(r'templates', TaxTemplateViewSet)
router.register(r'costcenters', CostCenterViewSet)
router.register(r'salesinvoices', SalesInvoiceViewSet)
router.register(r'purchaseinvoices', PurchaseInvoiceViewSet)
router.register(r'journalentries', JournalEntryViewSet)
router.register(r'journalentrylines', JournalEntryLineViewSet)
router.register(r'paymententries', PaymentEntryViewSet)
router.register(r'bankaccounts', BankAccountViewSet)
router.register(r'bankreconciliations', BankReconciliationViewSet)
router.register(r'subscriptionplans', SubscriptionPlanViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'shareholders', ShareholderViewSet)
router.register(r'sharetransfers', ShareTransferViewSet)
router.register(r'reports', ReportsViewSet, basename='reports')

urlpatterns = [
    path('', include(router.urls)),
    
]
