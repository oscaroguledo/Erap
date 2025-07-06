from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemGroupViewSet, BrandViewSet, UnitOfMeasureViewSet, ItemViewSet, WarehouseViewSet,
    StockLedgerEntryViewSet, StockEntryViewSet, StockBalanceViewSet, StockOpeningBalanceViewSet,
    BatchViewSet, InventorySerialNumberViewSet, StockEntryItemViewSet
)

router = DefaultRouter()
router.register(r'item-groups', ItemGroupViewSet, basename='itemgroup')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'units-of-measure', UnitOfMeasureViewSet, basename='unitofmeasure')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'stock-ledger-entries', StockLedgerEntryViewSet, basename='stockledgerentry')
router.register(r'stock-entries', StockEntryViewSet, basename='stockentry')
router.register(r'stock-balances', StockBalanceViewSet, basename='stockbalance')
router.register(r'stock-opening-balances', StockOpeningBalanceViewSet, basename='stockopeningbalance')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'serial-numbers', InventorySerialNumberViewSet, basename='serialnumber')
router.register(r'stock-entry-items', StockEntryItemViewSet, basename='stockentryitem')

urlpatterns = [
    path('', include(router.urls)),
]
