from rest_framework import serializers
from .models import (
    AssetCategory, AssetLocation, Asset, AssetDepreciation,
    AssetMaintenanceTeam, AssetMaintenance, AssetMaintenanceLog, AssetValueAdjustment
)

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'


class AssetLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetLocation
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    category = AssetCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetCategory.objects.all(), source='category', write_only=True)
    location = AssetLocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetLocation.objects.all(), source='location', write_only=True, allow_null=True, required=False)

    class Meta:
        model = Asset
        fields = [
            'id', 'asset_tag', 'name', 'category', 'category_id', 'location', 'location_id',
            'purchase_date', 'purchase_cost', 'current_value', 'salvage_value', 'useful_life_months',
            'is_active', 'notes', 'created_at', 'updated_at',
        ]


class AssetDepreciationSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(), source='asset', write_only=True)

    class Meta:
        model = AssetDepreciation
        fields = [
            'id', 'asset', 'asset_id', 'depreciation_date', 'depreciation_amount',
            'accumulated_depreciation', 'net_book_value',
        ]


class AssetMaintenanceTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetMaintenanceTeam
        fields = '__all__'


class AssetMaintenanceSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(), source='asset', write_only=True)
    maintenance_team = AssetMaintenanceTeamSerializer(read_only=True)
    maintenance_team_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetMaintenanceTeam.objects.all(), source='maintenance_team', write_only=True, allow_null=True, required=False)

    class Meta:
        model = AssetMaintenance
        fields = [
            'id', 'asset', 'asset_id', 'maintenance_team', 'maintenance_team_id',
            'maintenance_date', 'description', 'cost', 'next_due_date', 'remarks',
        ]


class AssetMaintenanceLogSerializer(serializers.ModelSerializer):
    maintenance = AssetMaintenanceSerializer(read_only=True)
    maintenance_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetMaintenance.objects.all(), source='maintenance', write_only=True)

    class Meta:
        model = AssetMaintenanceLog
        fields = [
            'id', 'maintenance', 'maintenance_id', 'log_date', 'description',
        ]


class AssetValueAdjustmentSerializer(serializers.ModelSerializer):
    asset = AssetSerializer(read_only=True)
    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(), source='asset', write_only=True)

    class Meta:
        model = AssetValueAdjustment
        fields = [
            'id', 'asset', 'asset_id', 'adjustment_date', 'adjustment_amount', 'reason', 'remarks',
        ]
