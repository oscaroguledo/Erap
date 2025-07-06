from rest_framework import serializers
from .models import (
    Company, Account, FiscalYear, PaymentTerm, PaymentMode,
    TaxCategory, TaxTemplate, CostCenter, SalesInvoice, PurchaseInvoice,
    JournalEntry, JournalEntryLine, PaymentEntry, BankAccount,
    BankReconciliation, SubscriptionPlan, Subscription,
    Shareholder, ShareTransfer, Supplier, PurchaseInvoiceItem, Customer, Item, SalesInvoiceItem, LedgerEntry
)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalYear
        fields = '__all__'

class PaymentTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerm
        fields = '__all__'

class PaymentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = '__all__'

class TaxCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxCategory
        fields = '__all__'

class TaxTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxTemplate
        fields = '__all__'

class CostCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCenter
        fields = '__all__'

class SalesInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoice
        fields = '__all__'

class PurchaseInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoice
        fields = '__all__'

class JournalEntryLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntryLine
        fields = '__all__'

class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True, read_only=True)
    class Meta:
        model = JournalEntry
        fields = '__all__'

class PaymentEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentEntry
        fields = '__all__'

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class BankReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankReconciliation
        fields = '__all__'

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class ShareholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shareholder
        fields = '__all__'

class ShareTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareTransfer
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class PurchaseInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInvoiceItem
        fields = '__all__'

class SalesInvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesInvoiceItem
        fields = '__all__'

class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = '__all__'

class TrialBalanceSerializer(serializers.Serializer):
    account = serializers.CharField()
    debit = serializers.DecimalField(max_digits=12, decimal_places=2)
    credit = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

class ProfitAndLossSerializer(serializers.Serializer):
    revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_or_loss = serializers.DecimalField(max_digits=12, decimal_places=2)
class AccountsReceivableSerializer(serializers.Serializer):
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_payments_received = serializers.DecimalField(max_digits=12, decimal_places=2)
    outstanding_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
class GrossProfitSerializer(serializers.Serializer):
    total_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    gross_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
class SalesTrendItemSerializer(serializers.Serializer):
    period = serializers.DateTimeField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)

class PaginatedSalesTrendSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    next_page = serializers.CharField(allow_null=True)
    prev_page = serializers.CharField(allow_null=True)
    data = SalesTrendItemSerializer(many=True)
class PurchaseTrendItemSerializer(serializers.Serializer):
    period = serializers.DateTimeField()
    total_purchases = serializers.DecimalField(max_digits=12, decimal_places=2)

class PaginatedPurchaseTrendSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    next_page = serializers.CharField(allow_null=True)
    prev_page = serializers.CharField(allow_null=True)
    data = PurchaseTrendItemSerializer(many=True)


