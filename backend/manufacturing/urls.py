from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet, BillOfMaterialsViewSet, BOMComponentViewSet, WorkstationTypeViewSet,
    WorkstationViewSet, OperationViewSet, RoutingViewSet, RoutingOperationViewSet,
    ProductionPlanViewSet, WorkOrderViewSet, JobCardViewSet,
    DowntimeEntryViewSet, StockEntryViewSet
)

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'bill-of-materials', BillOfMaterialsViewSet)
router.register(r'bom-components', BOMComponentViewSet)
router.register(r'workstation-types', WorkstationTypeViewSet)
router.register(r'workstations', WorkstationViewSet)
router.register(r'operations', OperationViewSet)
router.register(r'routings', RoutingViewSet)
router.register(r'routing-operations', RoutingOperationViewSet)
router.register(r'production-plans', ProductionPlanViewSet)
router.register(r'work-orders', WorkOrderViewSet)
router.register(r'job-cards', JobCardViewSet)
router.register(r'downtime-entries', DowntimeEntryViewSet)
router.register(r'stock-entries', StockEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
