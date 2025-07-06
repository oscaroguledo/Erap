from rest_framework import viewsets, pagination, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import (
    ProjectType, Project, Milestone, Task, ProjectUpdate,
    ActivityType, ActivityCost, Timesheet,
    ProjectExpense, ProjectInvoice
)
from .serializers import (
    ProjectTypeSerializer, ProjectSerializer, MilestoneSerializer,
    TaskSerializer, ProjectUpdateSerializer,
    ActivityTypeSerializer, ActivityCostSerializer, TimesheetSerializer,
    ProjectExpenseSerializer, ProjectInvoiceSerializer
)
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


@extend_schema(tags=['Project Types'])
class ProjectTypeViewSet(CustomResponseModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


@extend_schema(tags=['Projects'])
class ProjectViewSet(CustomResponseModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@extend_schema(tags=['Milestones'])
class MilestoneViewSet(CustomResponseModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer


@extend_schema(tags=['Tasks'])
class TaskViewSet(CustomResponseModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


@extend_schema(tags=['Project Updates'])
class ProjectUpdateViewSet(CustomResponseModelViewSet):
    queryset = ProjectUpdate.objects.all()
    serializer_class = ProjectUpdateSerializer


@extend_schema(tags=['Activity Types'])
class ActivityTypeViewSet(CustomResponseModelViewSet):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer


@extend_schema(tags=['Activity Costs'])
class ActivityCostViewSet(CustomResponseModelViewSet):
    queryset = ActivityCost.objects.all()
    serializer_class = ActivityCostSerializer


@extend_schema(tags=['Timesheets'])
class TimesheetViewSet(CustomResponseModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer


@extend_schema(tags=['Project Expenses'])
class ProjectExpenseViewSet(CustomResponseModelViewSet):
    queryset = ProjectExpense.objects.all()
    serializer_class = ProjectExpenseSerializer


@extend_schema(tags=['Project Invoices'])
class ProjectInvoiceViewSet(CustomResponseModelViewSet):
    queryset = ProjectInvoice.objects.all()
    serializer_class = ProjectInvoiceSerializer
