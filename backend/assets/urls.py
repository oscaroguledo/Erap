from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssetCategoryViewSet,
    AssetLocationViewSet,
    AssetViewSet,
    AssetDepreciationViewSet,
    AssetMaintenanceTeamViewSet,
    AssetMaintenanceViewSet,
    AssetMaintenanceLogViewSet,
    AssetValueAdjustmentViewSet,
)

router = DefaultRouter()
router.register(r'asset-categories', AssetCategoryViewSet, basename='assetcategory')
router.register(r'asset-locations', AssetLocationViewSet, basename='assetlocation')
router.register(r'assets', AssetViewSet, basename='asset')
router.register(r'asset-depreciations', AssetDepreciationViewSet, basename='assetdepreciation')
router.register(r'asset-maintenance-teams', AssetMaintenanceTeamViewSet, basename='assetmaintenanceteam')
router.register(r'asset-maintenances', AssetMaintenanceViewSet, basename='assetmaintenance')
router.register(r'asset-maintenance-logs', AssetMaintenanceLogViewSet, basename='assetmaintenancelog')
router.register(r'asset-value-adjustments', AssetValueAdjustmentViewSet, basename='assetvalueadjustment')

urlpatterns = [
    path('', include(router.urls)),
]
