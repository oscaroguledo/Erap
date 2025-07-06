from rest_framework import viewsets, status, pagination
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import (
    SalesPartner,
    ProductBundle,
    SalesOrder, SalesOrderItem,
    Quotation, QuotationItem,
    SalesInvoice, SalesInvoiceItem,
    POSProfile, POSSettings, LoyaltyPointEntry
)
from crm.models import Customer, CustomerGroup, Contact, Address, SalesPerson
from inventory.models import Item, ItemGroup

from .serializers import (
    SalesPartnerSerializer,
    ProductBundleSerializer,
    SalesOrderSerializer, SalesOrderItemSerializer,
    QuotationSerializer, QuotationItemSerializer,
    SalesInvoiceSerializer, SalesInvoiceItemSerializer,
    POSProfileSerializer, POSSettingsSerializer, LoyaltyPointEntrySerializer
)

from crm.serializers import CustomerGroupSerializer, CustomerSerializer, ContactSerializer, AddressSerializer, SalesPersonSerializer
from inventory.serializers import ItemGroupSerializer, ItemSerializer

from backend.utils.response import Response
from drf_spectacular.openapi import AutoSchema

class CustomSchema(AutoSchema):
    pass

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomResponseModelViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    schema = CustomSchema()

    @extend_schema(
        summary="List all objects",
        description="Returns a paginated list of objects",
        responses={200: OpenApiResponse(description="List of objects")}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Retrieve an object by ID",
        description="Returns the details of a specific object by its ID",
        responses={200: OpenApiResponse(description="Object details")}
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Create an object",
        description="Creates a new object with the provided data",
        responses={
            201: OpenApiResponse(description="Object created successfully"),
            400: OpenApiResponse(description="Invalid input data")
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update an object",
        description="Updates an existing object by ID. Supports full and partial updates.",
        responses={
            200: OpenApiResponse(description="Object updated successfully"),
            400: OpenApiResponse(description="Invalid input data"),
            404: OpenApiResponse(description="Object not found")
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data)

    @extend_schema(
        summary="Delete an object",
        description="Deletes an object by ID",
        responses={
            204: OpenApiResponse(description="Object deleted successfully"),
            404: OpenApiResponse(description="Object not found")
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# Now individual ViewSets for each model

@extend_schema(summary="Manage Customer Groups", description="CRUD operations for Customer Groups", tags=["Sales"])
class CustomerGroupViewSet(CustomResponseModelViewSet):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer

@extend_schema(summary="Manage Customers", description="CRUD operations for Customers", tags=["Sales"])
class CustomerViewSet(CustomResponseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@extend_schema(summary="Manage Contacts", description="CRUD operations for Contacts", tags=["Sales"])
class ContactViewSet(CustomResponseModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

@extend_schema(summary="Manage Addresses", description="CRUD operations for Addresses", tags=["Sales"])
class AddressViewSet(CustomResponseModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

@extend_schema(summary="Manage Sales Persons", description="CRUD operations for Sales Persons", tags=["Sales"])
class SalesPersonViewSet(CustomResponseModelViewSet):
    queryset = SalesPerson.objects.all()
    serializer_class = SalesPersonSerializer

@extend_schema(summary="Manage Sales Partners", description="CRUD operations for Sales Partners", tags=["Sales"])
class SalesPartnerViewSet(CustomResponseModelViewSet):
    queryset = SalesPartner.objects.all()
    serializer_class = SalesPartnerSerializer

@extend_schema(summary="Manage Item Groups", description="CRUD operations for Item Groups", tags=["Sales"])
class ItemGroupViewSet(CustomResponseModelViewSet):
    queryset = ItemGroup.objects.all()
    serializer_class = ItemGroupSerializer

@extend_schema(summary="Manage Items", description="CRUD operations for Items", tags=["Sales"])
class ItemViewSet(CustomResponseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

@extend_schema(summary="Manage Product Bundles", description="CRUD operations for Product Bundles", tags=["Sales"])
class ProductBundleViewSet(CustomResponseModelViewSet):
    queryset = ProductBundle.objects.all()
    serializer_class = ProductBundleSerializer

@extend_schema(summary="Manage Sales Orders", description="CRUD operations for Sales Orders", tags=["Sales"])
class SalesOrderViewSet(CustomResponseModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer

@extend_schema(summary="Manage Sales Order Items", description="CRUD operations for Sales Order Items", tags=["Sales"])
class SalesOrderItemViewSet(CustomResponseModelViewSet):
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer

@extend_schema(summary="Manage Quotations", description="CRUD operations for Quotations", tags=["Sales"])
class QuotationViewSet(CustomResponseModelViewSet):
    queryset = Quotation.objects.all()
    serializer_class = QuotationSerializer

@extend_schema(summary="Manage Quotation Items", description="CRUD operations for Quotation Items", tags=["Sales"])
class QuotationItemViewSet(CustomResponseModelViewSet):
    queryset = QuotationItem.objects.all()
    serializer_class = QuotationItemSerializer

@extend_schema(summary="Manage Sales Invoices", description="CRUD operations for Sales Invoices", tags=["Sales"])
class SalesInvoiceViewSet(CustomResponseModelViewSet):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer

@extend_schema(summary="Manage Sales Invoice Items", description="CRUD operations for Sales Invoice Items", tags=["Sales"])
class SalesInvoiceItemViewSet(CustomResponseModelViewSet):
    queryset = SalesInvoiceItem.objects.all()
    serializer_class = SalesInvoiceItemSerializer

@extend_schema(summary="Manage POS Profiles", description="CRUD operations for POS Profiles", tags=["Sales"])
class POSProfileViewSet(CustomResponseModelViewSet):
    queryset = POSProfile.objects.all()
    serializer_class = POSProfileSerializer

@extend_schema(summary="Manage POS Settings", description="CRUD operations for POS Settings", tags=["Sales"])
class POSSettingsViewSet(CustomResponseModelViewSet):
    queryset = POSSettings.objects.all()
    serializer_class = POSSettingsSerializer

@extend_schema(summary="Manage Loyalty Point Entries", description="CRUD operations for Loyalty Point Entries", tags=["Sales"])
class LoyaltyPointEntryViewSet(CustomResponseModelViewSet):
    queryset = LoyaltyPointEntry.objects.all()
    serializer_class = LoyaltyPointEntrySerializer
