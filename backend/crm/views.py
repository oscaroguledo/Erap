from rest_framework import viewsets, status, decorators,pagination
from .models import (
    Lead, Opportunity, Customer, Appointment, Communication,
    Territory, CustomerGroup, Contact, Prospect,
    SalesPerson, LeadSource, Campaign, CampaignResult,
    CRMSettings, MaintenanceVisit, WarrantyClaim
)
from .serializers import (
    LeadSerializer, OpportunitySerializer, CustomerSerializer,
    AppointmentSerializer, CommunicationSerializer,
    TerritorySerializer, CustomerGroupSerializer, ContactSerializer,
    ProspectSerializer, SalesPersonSerializer, LeadSourceSerializer,
    CampaignSerializer, CampaignResultSerializer,
    CRMSettingsSerializer, CrmMaintenanceVisitSerializer, CrmWarrantyClaimSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from datetime import timedelta
from django.utils import timezone
from django.db.models import functions, Sum, F, Value, Case, When, DecimalField, ExpressionWrapper
from drf_spectacular.openapi import AutoSchema


from backend.utils.response import Response
class CustomSchema(AutoSchema):
    # Optionally override methods here to customize the schema generation,
    # for example, add extra responses, descriptions, etc.
    pass

# Create your views here.
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10  # default items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class CustomResponseModelViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    schema = CustomSchema()

    @extend_schema(
        summary="List all objects",
        description="Returns a paginated list of objects",
        responses={200: OpenApiResponse(description="List of objects")}
        # You can specify request, parameters, etc.
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
        request=None,
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
        request=None,
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
    

# Apply to each ViewSet:
@extend_schema(
    summary="Manage Leads",
    description="CRUD operations for managing leads in the CRM.",
    tags=["CRM"]
)
class LeadViewSet(CustomResponseModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


@extend_schema(
    summary="Manage Opportunities",
    description="Track sales opportunities tied to leads or customers.",
    tags=["CRM", "Sales Pipeline"]
)
class OpportunityViewSet(CustomResponseModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer


@extend_schema(
    summary="Manage Customers",
    description="Customer data including territory, contact, and customer group.",
    tags=["CRM"]
)
class CustomerViewSet(CustomResponseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@extend_schema(
    summary="Manage Appointments",
    description="Schedule and view appointments for customers or opportunities.",
    tags=["CRM"]
)
class AppointmentViewSet(CustomResponseModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


@extend_schema(
    summary="Manage Communications",
    description="Call, email, and meeting logs tied to customers.",
    tags=["CRM"]
)
class CommunicationViewSet(CustomResponseModelViewSet):
    queryset = Communication.objects.all()
    serializer_class = CommunicationSerializer


@extend_schema(
    summary="Manage Territories",
    description="Define sales territories to categorize customers and leads.",
    tags=["Masters"]
)
class TerritoryViewSet(CustomResponseModelViewSet):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer


@extend_schema(
    summary="Manage Customer Groups",
    description="Segment customers based on shared attributes or categories.",
    tags=["Masters"]
)
class CustomerGroupViewSet(CustomResponseModelViewSet):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer


@extend_schema(
    summary="Manage Contacts",
    description="Contact persons related to customers or prospects.",
    tags=["CRM"]
)
class ContactViewSet(CustomResponseModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


@extend_schema(
    summary="Manage Prospects",
    description="Track early-stage potential customers.",
    tags=["CRM"]
)
class ProspectViewSet(CustomResponseModelViewSet):
    queryset = Prospect.objects.all()
    serializer_class = ProspectSerializer


@extend_schema(
    summary="Manage Sales Persons",
    description="Sales users and their commission structures.",
    tags=["Masters"]
)
class SalesPersonViewSet(CustomResponseModelViewSet):
    queryset = SalesPerson.objects.all()
    serializer_class = SalesPersonSerializer


@extend_schema(
    summary="Manage Lead Sources",
    description="Define channels from which leads originate.",
    tags=["Masters"]
)
class LeadSourceViewSet(CustomResponseModelViewSet):
    queryset = LeadSource.objects.all()
    serializer_class = LeadSourceSerializer


@extend_schema(
    summary="Manage Campaigns",
    description="Marketing campaigns that generate leads.",
    tags=["Campaign"]
)
class CampaignViewSet(CustomResponseModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


@extend_schema(
    summary="Manage Campaign Results",
    description="Track metrics and KPIs from campaigns.",
    tags=["Campaign"]
)
class CampaignResultViewSet(CustomResponseModelViewSet):
    queryset = CampaignResult.objects.all()
    serializer_class = CampaignResultSerializer


@extend_schema(
    summary="CRM Settings",
    description="Default configuration for lead routing and auto-archiving.",
    tags=["Settings"]
)
class CRMSettingsViewSet(CustomResponseModelViewSet):
    queryset = CRMSettings.objects.all()
    serializer_class = CRMSettingsSerializer


@extend_schema(
    summary="Manage Maintenance Visits",
    description="Log visits for customer service or support.",
    tags=["Maintenance"]
)
class MaintenanceVisitViewSet(CustomResponseModelViewSet):
    queryset = MaintenanceVisit.objects.all()
    serializer_class = CrmMaintenanceVisitSerializer


@extend_schema(
    summary="Manage Warranty Claims",
    description="Track product warranty issues and their resolutions.",
    tags=["Maintenance"]
)
class WarrantyClaimViewSet(CustomResponseModelViewSet):
    queryset = WarrantyClaim.objects.all()
    serializer_class = CrmWarrantyClaimSerializer