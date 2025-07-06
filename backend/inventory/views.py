from rest_framework import viewsets, status, pagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import AutoSchema
from .models import (
    ItemGroup, Brand, UnitOfMeasure, Item, Warehouse,
    StockLedgerEntry, StockEntry, StockBalance, StockOpeningBalance,
    Batch, InventorySerialNumber, StockEntryItem
)
from .serializers import (
    ItemGroupSerializer, BrandSerializer, UnitOfMeasureSerializer, ItemSerializer, WarehouseSerializer,
    StockLedgerEntrySerializer, StockEntrySerializer, StockBalanceSerializer, StockOpeningBalanceSerializer,
    BatchSerializer, InventorySerialNumberSerializer, StockEntryItemSerializer
)
from backend.utils.response import Response

class CustomSchema(AutoSchema):
    pass

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomResponseModelViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    schema = CustomSchema()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page else self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Manage Item Groups",
    description="Create, retrieve, update, and delete item groups used to categorize inventory items.",
    tags=["Masters"]
)
class ItemGroupViewSet(CustomResponseModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer

@extend_schema(
    summary="Manage Brands",
    description="Create, retrieve, update, and delete product brands.",
    tags=["Masters"]
)
class BrandViewSet(CustomResponseModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

@extend_schema(
    summary="Manage Units of Measure",
    description="Manage units of measure used across inventory items (e.g., kg, liter, piece).",
    tags=["Masters"]
)
class UnitOfMeasureViewSet(CustomResponseModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer

@extend_schema(
    summary="Manage Inventory Items",
    description="CRUD operations for inventory items including SKU, description, brand, unit of measure, and reorder levels.",
    tags=["Inventory"]
)
class ItemViewSet(CustomResponseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

@extend_schema(
    summary="Manage Warehouses",
    description="Create and manage warehouses where stock is stored.",
    tags=["Inventory"]
)
class WarehouseViewSet(CustomResponseModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

@extend_schema(
    summary="Stock Ledger Entries",
    description="Track detailed stock movement transactions for items across warehouses.",
    tags=["Inventory"]
)
class StockLedgerEntryViewSet(CustomResponseModelViewSet):
    queryset = StockLedgerEntry.objects.all()
    serializer_class = StockLedgerEntrySerializer

@extend_schema(
    summary="Stock Entries",
    description="Record stock movements such as receipts, issues, transfers, repackaging, and adjustments.",
    tags=["Inventory"]
)
class StockEntryViewSet(CustomResponseModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class = StockEntrySerializer

@extend_schema(
    summary="Stock Balances",
    description="View current stock quantities per item per warehouse (denormalized for quick lookups).",
    tags=["Inventory"]
)
class StockBalanceViewSet(CustomResponseModelViewSet):
    queryset = StockBalance.objects.all()
    serializer_class = StockBalanceSerializer

@extend_schema(
    summary="Stock Opening Balances",
    description="Set or update initial stock balances for items when starting stock tracking.",
    tags=["Inventory"]
)
class StockOpeningBalanceViewSet(CustomResponseModelViewSet):
    queryset = StockOpeningBalance.objects.all()
    serializer_class = StockOpeningBalanceSerializer

@extend_schema(
    summary="Batch Management",
    description="Manage batches of items including manufacture and expiry dates.",
    tags=["Inventory"]
)
class BatchViewSet(CustomResponseModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

@extend_schema(
    summary="Serial Number Management",
    description="Track serial numbers for items, including status, warranty expiry, and batch association.",
    tags=["Inventory"]
)
class InventorySerialNumberViewSet(CustomResponseModelViewSet):
    queryset = InventorySerialNumber.objects.all()
    serializer_class = InventorySerialNumberSerializer

@extend_schema(
    summary="Stock Entry Items",
    description="Manage individual items within a stock entry, including batch and serial number associations.",
    tags=["Inventory"]
)
class StockEntryItemViewSet(CustomResponseModelViewSet):
    queryset = StockEntryItem.objects.all()
    serializer_class = StockEntryItemSerializer
