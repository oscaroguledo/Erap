from rest_framework import serializers
from rest_framework import serializers
from .models import (
    SalesPartner, ProductBundle, ProductBundleItem,
    SalesOrder, SalesOrderItem, Quotation, QuotationItem,
    SalesInvoice, SalesInvoiceItem, POSProfile, POSSettings, LoyaltyPointEntry
)



class SalesPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesPartner
        fields = ['id', 'code', 'name', 'commission_percent']
class ProductBundleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBundleItem
        fields = ['id', 'product_bundle', 'item', 'quantity']


class ProductBundleSerializer(serializers.ModelSerializer):
    items = ProductBundleItemSerializer(source='productbundleitem_set', many=True, read_only=True)

    class Meta:
        model = ProductBundle
        fields = ['id', 'name', 'description', 'items']
class SalesOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderItem
        fields = ['id', 'sales_order', 'item', 'quantity', 'rate', 'amount']


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'customer', 'sales_person', 'sales_partner',
            'order_date', 'delivery_date', 'status', 'total_amount', 'remarks', 'items'
        ]
class QuotationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItem
        fields = ['id', 'quotation', 'item', 'quantity', 'rate', 'amount']


class QuotationSerializer(serializers.ModelSerializer):
    items = QuotationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = [
            'id', 'quotation_number', 'customer', 'sales_person',
            'quotation_date', 'valid_until', 'status', 'total_amount', 'remarks', 'items'
        ]
class SalesInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceItem
        fields = ['id', 'sales_invoice', 'item', 'quantity', 'rate', 'amount']


class SalesInvoiceSerializer(serializers.ModelSerializer):
    items = SalesInvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = SalesInvoice
        fields = [
            'id', 'invoice_number', 'sales_order', 'customer',
            'invoice_date', 'due_date', 'status', 'total_amount', 'remarks', 'items'
        ]
class POSProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSProfile
        fields = ['id', 'name', 'location', 'active']


class POSSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSSettings
        fields = ['id', 'pos_profile', 'loyalty_enabled']


class LoyaltyPointEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyPointEntry
        fields = ['id', 'customer', 'points', 'entry_date', 'remarks']
