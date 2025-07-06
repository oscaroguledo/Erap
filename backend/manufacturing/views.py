from rest_framework import viewsets, status, pagination
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema

from .models import (
    Item, BillOfMaterials, BOMComponent, WorkstationType, Workstation,
    Operation, Routing, RoutingOperation, ProductionPlan,
    WorkOrder, JobCard, DowntimeEntry, StockEntry
)
from .serializers import (
    ItemSerializer, BillOfMaterialsSerializer, BOMComponentSerializer, WorkstationTypeSerializer,
    WorkstationSerializer, OperationSerializer, RoutingSerializer, RoutingOperationSerializer,
    ProductionPlanSerializer, WorkOrderSerializer, JobCardSerializer, DowntimeEntrySerializer,
    StockEntrySerializer
)


from backend.utils.response import Response

# Custom schema class (can be enhanced later)
class CustomSchema(AutoSchema):
    pass


# Pagination class
class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Base viewset with response wrapping
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
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Manage Items",
    description="Create, retrieve, update, delete, and list inventory items including raw materials and finished goods.",
    tags=["Items"]
)
class ItemViewSet(CustomResponseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

@extend_schema(
    summary="Manage Bill of Materials",
    description="Create, update, delete, and list BOMs linking finished goods with their components.",
    tags=["Bill of Materials"]
)
class BillOfMaterialsViewSet(CustomResponseModelViewSet):
    queryset = BillOfMaterials.objects.all()
    serializer_class = BillOfMaterialsSerializer

@extend_schema(
    summary="Manage BOM Components",
    description="Manage components used in each Bill of Materials.",
    tags=["Bill of Materials"]
)
class BOMComponentViewSet(CustomResponseModelViewSet):
    queryset = BOMComponent.objects.all()
    serializer_class = BOMComponentSerializer

@extend_schema(
    summary="Manage Workstation Types",
    description="Create and manage different types of workstations in the production environment.",
    tags=["Workstations"]
)
class WorkstationTypeViewSet(CustomResponseModelViewSet):
    queryset = WorkstationType.objects.all()
    serializer_class = WorkstationTypeSerializer

@extend_schema(
    summary="Manage Workstations",
    description="Manage individual workstations assigned to specific workstation types.",
    tags=["Workstations"]
)
class WorkstationViewSet(CustomResponseModelViewSet):
    queryset = Workstation.objects.all()
    serializer_class = WorkstationSerializer

@extend_schema(
    summary="Manage Operations",
    description="Create and manage production operations linked to workstation types.",
    tags=["Operations"]
)
class OperationViewSet(CustomResponseModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer

@extend_schema(
    summary="Manage Routings",
    description="Manage routing sequences of operations required to produce items.",
    tags=["Routing"]
)
class RoutingViewSet(CustomResponseModelViewSet):
    queryset = Routing.objects.all()
    serializer_class = RoutingSerializer

@extend_schema(
    summary="Manage Routing Operations",
    description="Manage operation sequences within a routing.",
    tags=["Routing"]
)
class RoutingOperationViewSet(CustomResponseModelViewSet):
    queryset = RoutingOperation.objects.all()
    serializer_class = RoutingOperationSerializer

@extend_schema(
    summary="Manage Production Plans",
    description="Create, update, delete and list production plans for items.",
    tags=["Production"]
)
class ProductionPlanViewSet(CustomResponseModelViewSet):
    queryset = ProductionPlan.objects.all()
    serializer_class = ProductionPlanSerializer

@extend_schema(
    summary="Manage Work Orders",
    description="Create, update, delete and list work orders associated with production plans.",
    tags=["Production"]
)
class WorkOrderViewSet(CustomResponseModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

@extend_schema(
    summary="Manage Job Cards",
    description="Manage job cards for tracking operations performed on work orders.",
    tags=["Production"]
)
class JobCardViewSet(CustomResponseModelViewSet):
    queryset = JobCard.objects.all()
    serializer_class = JobCardSerializer

@extend_schema(
    summary="Manage Downtime Entries",
    description="Record and track downtime events for workstations.",
    tags=["Production"]
)
class DowntimeEntryViewSet(CustomResponseModelViewSet):
    queryset = DowntimeEntry.objects.all()
    serializer_class = DowntimeEntrySerializer

@extend_schema(
    summary="Manage Stock Entries",
    description="Manage stock in and out entries for inventory items.",
    tags=["Inventory"]
)
class StockEntryViewSet(CustomResponseModelViewSet):
    queryset = StockEntry.objects.all()
    serializer_class = StockEntrySerializer
