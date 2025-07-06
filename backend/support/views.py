from rest_framework import viewsets, pagination, status
from backend.utils.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import (
    Issue, IssueType, MaintenanceVisit, ServiceLevelAgreement, WarrantyClaim, SupportSerialNumber
)
from .serializers import (
    IssueSerializer, IssueTypeSerializer, SupportMaintenanceVisitSerializer,
    ServiceLevelAgreementSerializer, SupportWarrantyClaimSerializer, SupportSerialNumberSerializer
)
from drf_spectacular.openapi import AutoSchema


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CustomSchema(AutoSchema):
    pass


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
        summary="Create a new object",
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
        summary="Update an existing object",
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


@extend_schema(
    summary="Manage Issue Types",
    description="Create, list, update, and delete types of issues.",
    tags=["Issue Management"]
)
class IssueTypeViewSet(CustomResponseModelViewSet):
    queryset = IssueType.objects.all()
    serializer_class = IssueTypeSerializer


@extend_schema(
    summary="Manage Issues",
    description="Create, list, update, and delete issues reported.",
    tags=["Issue Management"]
)
class IssueViewSet(CustomResponseModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


@extend_schema(
    summary="Manage Maintenance Visits",
    description="Track maintenance visits and related information.",
    tags=["Maintenance"]
)
class MaintenanceVisitViewSet(CustomResponseModelViewSet):
    queryset = MaintenanceVisit.objects.all()
    serializer_class = SupportMaintenanceVisitSerializer


@extend_schema(
    summary="Manage Service Level Agreements",
    description="Define and manage service level agreements (SLAs).",
    tags=["Service Management"]
)
class ServiceLevelAgreementViewSet(CustomResponseModelViewSet):
    queryset = ServiceLevelAgreement.objects.all()
    serializer_class = ServiceLevelAgreementSerializer


@extend_schema(
    summary="Manage Warranty Claims",
    description="Create and track warranty claims.",
    tags=["Warranty"]
)
class WarrantyClaimViewSet(CustomResponseModelViewSet):
    queryset = WarrantyClaim.objects.all()
    serializer_class = SupportWarrantyClaimSerializer


@extend_schema(
    summary="Manage Serial Numbers",
    description="Manage serial numbers of products or assets.",
    tags=["Inventory"]
)
class SupportSerialNumberViewSet(CustomResponseModelViewSet):
    queryset = SupportSerialNumber.objects.all()
    serializer_class = SupportSerialNumberSerializer
