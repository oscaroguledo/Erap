from rest_framework import serializers
from .models import (
    Item, BillOfMaterials, BOMComponent, WorkstationType, Workstation,
    Operation, Routing, RoutingOperation, ProductionPlan,
    WorkOrder, JobCard, DowntimeEntry, StockEntry
)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class BOMComponentSerializer(serializers.ModelSerializer):
    component = ItemSerializer(read_only=True)
    component_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='component', write_only=True
    )

    class Meta:
        model = BOMComponent
        fields = ['id', 'component', 'component_id', 'quantity']

class BillOfMaterialsSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )
    components = BOMComponentSerializer(many=True, read_only=True)

    class Meta:
        model = BillOfMaterials
        fields = ['id', 'item', 'item_id', 'description', 'effective_from', 'effective_to', 'components']

class WorkstationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkstationType
        fields = '__all__'

class WorkstationSerializer(serializers.ModelSerializer):
    workstation_type = WorkstationTypeSerializer(read_only=True)
    workstation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkstationType.objects.all(), source='workstation_type', write_only=True
    )

    class Meta:
        model = Workstation
        fields = ['id', 'name', 'workstation_type', 'workstation_type_id', 'description']

class OperationSerializer(serializers.ModelSerializer):
    workstation_type = WorkstationTypeSerializer(read_only=True)
    workstation_type_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkstationType.objects.all(), source='workstation_type', write_only=True
    )

    class Meta:
        model = Operation
        fields = ['id', 'name', 'description', 'workstation_type', 'workstation_type_id']

class RoutingOperationSerializer(serializers.ModelSerializer):
    operation = OperationSerializer(read_only=True)
    operation_id = serializers.PrimaryKeyRelatedField(
        queryset=Operation.objects.all(), source='operation', write_only=True
    )

    class Meta:
        model = RoutingOperation
        fields = ['id', 'operation', 'operation_id', 'sequence']

class RoutingSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )
    operations = RoutingOperationSerializer(source='routingoperation_set', many=True, read_only=True)

    class Meta:
        model = Routing
        fields = ['id', 'item', 'item_id', 'description', 'operations']

class ProductionPlanSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = ProductionPlan
        fields = ['id', 'item', 'item_id', 'quantity', 'planned_start_date', 'planned_end_date', 'productionplan_status']

class WorkOrderSerializer(serializers.ModelSerializer):
    production_plan = ProductionPlanSerializer(read_only=True)
    production_plan_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductionPlan.objects.all(), source='production_plan', write_only=True
    )
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = WorkOrder
        fields = ['id', 'production_plan', 'production_plan_id', 'item', 'item_id', 'quantity', 'scheduled_start_date', 'scheduled_end_date', 'workorder_status']

class JobCardSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer(read_only=True)
    work_order_id = serializers.PrimaryKeyRelatedField(
        queryset=WorkOrder.objects.all(), source='work_order', write_only=True
    )
    operation = OperationSerializer(read_only=True)
    operation_id = serializers.PrimaryKeyRelatedField(
        queryset=Operation.objects.all(), source='operation', write_only=True
    )
    workstation = WorkstationSerializer(read_only=True)
    workstation_id = serializers.PrimaryKeyRelatedField(
        queryset=Workstation.objects.all(), source='workstation', write_only=True
    )

    class Meta:
        model = JobCard
        fields = ['id', 'work_order', 'work_order_id', 'operation', 'operation_id', 'workstation', 'workstation_id', 'start_time', 'end_time', 'jobcard_status', 'notes']

class DowntimeEntrySerializer(serializers.ModelSerializer):
    workstation = WorkstationSerializer(read_only=True)
    workstation_id = serializers.PrimaryKeyRelatedField(
        queryset=Workstation.objects.all(), source='workstation', write_only=True
    )

    class Meta:
        model = DowntimeEntry
        fields = ['id', 'workstation', 'workstation_id', 'start_time', 'end_time', 'reason']

class StockEntrySerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )

    class Meta:
        model = StockEntry
        fields = ['id', 'item', 'item_id', 'quantity', 'entry_type', 'date', 'reference']
