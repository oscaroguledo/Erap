from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerGroupViewSet, CustomerViewSet, ContactViewSet, AddressViewSet,
    SalesPersonViewSet, SalesPartnerViewSet,
    ItemGroupViewSet, ItemViewSet, ProductBundleViewSet,
    SalesOrderViewSet, SalesOrderItemViewSet,
    QuotationViewSet, QuotationItemViewSet,
    SalesInvoiceViewSet, SalesInvoiceItemViewSet,
    POSProfileViewSet, POSSettingsViewSet, LoyaltyPointEntryViewSet
)

router = DefaultRouter()

# Customer related routes
router.register(r'customer-groups', CustomerGroupViewSet, basename='customer-group')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'addresses', AddressViewSet, basename='address')

# Sales person and partner
router.register(r'sales-persons', SalesPersonViewSet, basename='sales-person')
router.register(r'sales-partners', SalesPartnerViewSet, basename='sales-partner')

# Item and bundles
router.register(r'item-groups', ItemGroupViewSet, basename='item-group')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'product-bundles', ProductBundleViewSet, basename='product-bundle')

# Sales documents
router.register(r'sales-orders', SalesOrderViewSet, basename='sales-order')
router.register(r'sales-order-items', SalesOrderItemViewSet, basename='sales-order-item')

router.register(r'quotations', QuotationViewSet, basename='quotation')
router.register(r'quotation-items', QuotationItemViewSet, basename='quotation-item')

router.register(r'sales-invoices', SalesInvoiceViewSet, basename='sales-invoice')
router.register(r'sales-invoice-items', SalesInvoiceItemViewSet, basename='sales-invoice-item')

# POS
router.register(r'pos-profiles', POSProfileViewSet, basename='pos-profile')
router.register(r'pos-settings', POSSettingsViewSet, basename='pos-settings')
router.register(r'loyalty-points', LoyaltyPointEntryViewSet, basename='loyalty-point-entry')


urlpatterns = [
    path('', include(router.urls)),
]
