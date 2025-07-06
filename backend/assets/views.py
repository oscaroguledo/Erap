from rest_framework import viewsets, status, pagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import (
    AssetCategory, AssetLocation, Asset, AssetDepreciation,
    AssetMaintenanceTeam, AssetMaintenance, AssetMaintenanceLog, AssetValueAdjustment
)
from .serializers import (
    AssetCategorySerializer, AssetLocationSerializer, AssetSerializer, AssetDepreciationSerializer,
    AssetMaintenanceTeamSerializer, AssetMaintenanceSerializer, AssetMaintenanceLogSerializer,
    AssetValueAdjustmentSerializer
)
from backend.utils.response import Response
from drf_spectacular.openapi import AutoSchema

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
    

@extend_schema(
    summary="Manage Asset Categories",
    description="Create, update, delete and list asset categories.",
    tags=["Assets"]
)
class AssetCategoryViewSet(CustomResponseModelViewSet):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer


@extend_schema(
    summary="Manage Asset Locations",
    description="Create, update, delete and list asset locations.",
    tags=["Assets"]
)
class AssetLocationViewSet(CustomResponseModelViewSet):
    queryset = AssetLocation.objects.all()
    serializer_class = AssetLocationSerializer


@extend_schema(
    summary="Manage Assets",
    description="Create, update, delete and list assets.",
    tags=["Assets"]
)
class AssetViewSet(CustomResponseModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


@extend_schema(
    summary="Manage Asset Depreciations",
    description="Create, update, delete and list asset depreciations.",
    tags=["Assets"]
)
class AssetDepreciationViewSet(CustomResponseModelViewSet):
    queryset = AssetDepreciation.objects.all()
    serializer_class = AssetDepreciationSerializer


@extend_schema(
    summary="Manage Asset Maintenance Teams",
    description="Create, update, delete and list asset maintenance teams.",
    tags=["Assets"]
)
class AssetMaintenanceTeamViewSet(CustomResponseModelViewSet):
    queryset = AssetMaintenanceTeam.objects.all()
    serializer_class = AssetMaintenanceTeamSerializer


@extend_schema(
    summary="Manage Asset Maintenances",
    description="Create, update, delete and list asset maintenance records.",
    tags=["Assets"]
)
class AssetMaintenanceViewSet(CustomResponseModelViewSet):
    queryset = AssetMaintenance.objects.all()
    serializer_class = AssetMaintenanceSerializer


@extend_schema(
    summary="Manage Asset Maintenance Logs",
    description="Create, update, delete and list asset maintenance logs.",
    tags=["Assets"]
)
class AssetMaintenanceLogViewSet(CustomResponseModelViewSet):
    queryset = AssetMaintenanceLog.objects.all()
    serializer_class = AssetMaintenanceLogSerializer


@extend_schema(
    summary="Manage Asset Value Adjustments",
    description="Create, update, delete and list asset value adjustments.",
    tags=["Assets"]
)
class AssetValueAdjustmentViewSet(CustomResponseModelViewSet):
    queryset = AssetValueAdjustment.objects.all()
    serializer_class = AssetValueAdjustmentSerializer
