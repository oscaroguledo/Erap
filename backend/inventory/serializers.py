from rest_framework import serializers
from .models import (
    ItemGroup, Brand, UnitOfMeasure, Item, Warehouse,
    StockLedgerEntry, StockEntry, StockBalance, StockOpeningBalance,
    Batch, InventorySerialNumber, StockEntryItem
)

# Simple serializers for master data

class ItemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemGroup
        fields = ['id', 'name', 'description', 'parent']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description']

class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = ['id', 'name', 'abbreviation']

class ItemSerializer(serializers.ModelSerializer):
    item_group = ItemGroupSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    unit_of_measure = UnitOfMeasureSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'sku', 'name', 'description', 'item_group', 'brand', 'unit_of_measure', 'is_active', 'reorder_level']

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'code', 'name', 'description', 'address', 'is_active']

class StockLedgerEntrySerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = StockLedgerEntry
        fields = ['id', 'item', 'warehouse', 'transaction_type', 'quantity', 'transaction_date', 'reference_doc', 'remarks']

class StockEntrySerializer(serializers.ModelSerializer):
    from_warehouse = WarehouseSerializer(read_only=True)
    to_warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = StockEntry
        fields = ['id', 'entry_type', 'posting_date', 'posting_time', 'from_warehouse', 'to_warehouse', 'reference_doc', 'remarks', 'created_at']

class StockBalanceSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = StockBalance
        fields = ['id', 'item', 'warehouse', 'quantity']

class StockOpeningBalanceSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = StockOpeningBalance
        fields = ['id', 'item', 'warehouse', 'quantity', 'posting_date', 'remarks']

# Batch serializer

class BatchSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'batch_number', 'item', 'manufacture_date', 'expiry_date', 'description']

# Serial Number serializer

class InventorySerialNumberSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    batch = BatchSerializer(read_only=True)

    class Meta:
        model = InventorySerialNumber
        fields = ['id', 'serial_number', 'item', 'batch', 'status', 'warranty_expiry_date', 'description']

# StockEntryItem serializer

class StockEntryItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    batch = BatchSerializer(read_only=True)
    serial_numbers = InventorySerialNumberSerializer(many=True, read_only=True)

    # To create/update nested relationships, allow IDs
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), source='item', write_only=True)
    batch_id = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all(), source='batch', write_only=True, allow_null=True, required=False)
    serial_numbers_ids = serializers.PrimaryKeyRelatedField(queryset=InventorySerialNumber.objects.all(), source='serial_numbers', many=True, write_only=True, required=False)

    class Meta:
        model = StockEntryItem
        fields = [
            'id', 'stock_entry', 'item', 'batch', 'serial_numbers',
            'quantity', 'uom',
            'item_id', 'batch_id', 'serial_numbers_ids'
        ]

    def create(self, validated_data):
        serial_numbers = validated_data.pop('serial_numbers', [])
        stock_entry_item = StockEntryItem.objects.create(**validated_data)
        if serial_numbers:
            stock_entry_item.serial_numbers.set(serial_numbers)
        return stock_entry_item

    def update(self, instance, validated_data):
        serial_numbers = validated_data.pop('serial_numbers', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if serial_numbers is not None:
            instance.serial_numbers.set(serial_numbers)
        return instance
