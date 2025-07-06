from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, status, decorators,pagination
from datetime import timedelta
from django.utils import timezone
from django.db.models import functions, Sum, F, Value, Case, When, DecimalField, ExpressionWrapper


from .models import (
    Company, Account, FiscalYear, PaymentTerm, PaymentMode,
    TaxCategory, TaxTemplate, CostCenter, SalesInvoice, PurchaseInvoice,
    JournalEntry, JournalEntryLine, PaymentEntry, BankAccount,
    BankReconciliation, SubscriptionPlan, Subscription,
    Shareholder, ShareTransfer,Supplier,LedgerEntry, Item, PurchaseInvoiceItem, SalesInvoiceItem, Customer
)
from .serializers import (
    CompanySerializer, AccountSerializer, FiscalYearSerializer, PaymentTermSerializer, PaymentModeSerializer,
    TaxCategorySerializer, TaxTemplateSerializer, CostCenterSerializer, SalesInvoiceSerializer, PurchaseInvoiceSerializer,
    JournalEntrySerializer, JournalEntryLineSerializer, PaymentEntrySerializer, BankAccountSerializer,
    BankReconciliationSerializer, SubscriptionPlanSerializer, SubscriptionSerializer,
    ShareholderSerializer, ShareTransferSerializer,SupplierSerializer,LedgerEntrySerializer,ItemSerializer,
    PurchaseInvoiceItemSerializer, SalesInvoiceItemSerializer,CustomerSerializer,TrialBalanceSerializer,
    PaginatedPurchaseTrendSerializer,PurchaseTrendItemSerializer,PaginatedSalesTrendSerializer,SalesTrendItemSerializer,
    GrossProfitSerializer,AccountsReceivableSerializer,ProfitAndLossSerializer
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
    summary="Manage companies",
    description="Create, retrieve, update, or delete companies in the ERP system.",
    tags=['Company']
)
class CompanyViewSet(CustomResponseModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    

@extend_schema(
    summary="Manage accounts",
    description="CRUD operations on chart of accounts.",
    tags=['Accounting']
)
class AccountViewSet(CustomResponseModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@extend_schema(
    summary="Manage fiscal years",
    description="Handle fiscal years including opening and closing periods.",
    tags=['Accounting']
)
class FiscalYearViewSet(CustomResponseModelViewSet):
    queryset = FiscalYear.objects.all()
    serializer_class = FiscalYearSerializer


@extend_schema(
    summary="Manage payment terms",
    description="Define payment terms for invoices and bills.",
    tags=['Payments']
)
class PaymentTermViewSet(CustomResponseModelViewSet):
    queryset = PaymentTerm.objects.all()
    serializer_class = PaymentTermSerializer


@extend_schema(
    summary="Manage payment modes",
    description="Create and update different payment modes (cash, cheque, bank transfer, etc.).",
    tags=['Payments']
)
class PaymentModeViewSet(CustomResponseModelViewSet):
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer


@extend_schema(
    summary="Manage tax categories",
    description="Create and manage categories for taxes.",
    tags=['Tax']
)
class TaxCategoryViewSet(CustomResponseModelViewSet):
    queryset = TaxCategory.objects.all()
    serializer_class = TaxCategorySerializer


@extend_schema(
    summary="Manage tax templates",
    description="Setup templates for tax calculations applied on invoices.",
    tags=['Tax']
)
class TaxTemplateViewSet(CustomResponseModelViewSet):
    queryset = TaxTemplate.objects.all()
    serializer_class = TaxTemplateSerializer


@extend_schema(
    summary="Manage cost centers",
    description="Define and allocate cost centers for budgeting and expense tracking.",
    tags=['Budgeting']
)
class CostCenterViewSet(CustomResponseModelViewSet):
    queryset = CostCenter.objects.all()
    serializer_class = CostCenterSerializer


@extend_schema(
    summary="Manage sales invoices",
    description="Create and track sales invoices.",
    tags=['Sales']
)
class SalesInvoiceViewSet(CustomResponseModelViewSet):
    queryset = SalesInvoice.objects.all()
    serializer_class = SalesInvoiceSerializer


@extend_schema(
    summary="Manage purchase invoices",
    description="Create and track purchase invoices.",
    tags=['Purchases']
)
class PurchaseInvoiceViewSet(CustomResponseModelViewSet):
    queryset = PurchaseInvoice.objects.all()
    serializer_class = PurchaseInvoiceSerializer


@extend_schema(
    summary="Manage journal entries",
    description="Record and manage journal entries in the accounting ledger.",
    tags=['Accounting']
)
class JournalEntryViewSet(CustomResponseModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer


@extend_schema(
    summary="Manage journal entry lines",
    description="Detailed lines within journal entries for debit and credit records.",
    tags=['Accounting']
)
class JournalEntryLineViewSet(CustomResponseModelViewSet):
    queryset = JournalEntryLine.objects.all()
    serializer_class = JournalEntryLineSerializer


@extend_schema(
    summary="Manage payment entries",
    description="Record payments received or made against invoices or bills.",
    tags=['Payments']
)
class PaymentEntryViewSet(CustomResponseModelViewSet):
    queryset = PaymentEntry.objects.all()
    serializer_class = PaymentEntrySerializer
@extend_schema(
    summary="Manage bank accounts",
    description="Create, retrieve, update, or delete bank accounts for the company.",
    tags=['Banking']
)
class BankAccountViewSet(CustomResponseModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


@extend_schema(
    summary="Manage bank reconciliations",
    description="Handle reconciliation of bank statements with internal records.",
    tags=['Banking']
)
class BankReconciliationViewSet(CustomResponseModelViewSet):
    queryset = BankReconciliation.objects.all()
    serializer_class = BankReconciliationSerializer


@extend_schema(
    summary="Manage subscription plans",
    description="Define subscription plans for services or products.",
    tags=['Subscription Management']
)
class SubscriptionPlanViewSet(CustomResponseModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer


@extend_schema(
    summary="Manage subscriptions",
    description="Create and manage active subscriptions for customers or users.",
    tags=['Subscription Management']
)
class SubscriptionViewSet(CustomResponseModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


@extend_schema(
    summary="Manage shareholders",
    description="CRUD operations for shareholders data and details.",
    tags=['Share Management']
)
class ShareholderViewSet(CustomResponseModelViewSet):
    queryset = Shareholder.objects.all()
    serializer_class = ShareholderSerializer


@extend_schema(
    summary="Manage share transfers",
    description="Track and manage transfers of shares between shareholders.",
    tags=['Share Management']
)
class ShareTransferViewSet(CustomResponseModelViewSet):
    queryset = ShareTransfer.objects.all()
    serializer_class = ShareTransferSerializer


# --- Supplier ---
@extend_schema(
    summary="Manage suppliers",
    description="Create, update, and view suppliers.",
    tags=['Purchases']
)
class SupplierViewSet(CustomResponseModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


# --- Customer ---
@extend_schema(
    summary="Manage customers",
    description="Create, update, and view customers.",
    tags=['Sales']
)
class CustomerViewSet(CustomResponseModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# --- Items ---
@extend_schema(
    summary="Manage items",
    description="Create and manage inventory items.",
    tags=['Inventory']
)
class ItemViewSet(CustomResponseModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# --- Purchase Invoice Items ---
@extend_schema(
    summary="Manage purchase invoice items",
    description="Track items included in purchase invoices.",
    tags=['Purchases']
)
class PurchaseInvoiceItemViewSet(CustomResponseModelViewSet):
    queryset = PurchaseInvoiceItem.objects.all()
    serializer_class = PurchaseInvoiceItemSerializer


# --- Sales Invoice Items ---
@extend_schema(
    summary="Manage sales invoice items",
    description="Track items included in sales invoices.",
    tags=['Sales']
)
class SalesInvoiceItemViewSet(CustomResponseModelViewSet):
    queryset = SalesInvoiceItem.objects.all()
    serializer_class = SalesInvoiceItemSerializer


# --- Ledger Entries ---
@extend_schema(
    summary="Manage ledger entries",
    description="Track debit and credit entries for customers and suppliers.",
    tags=['Accounting', 'Ledgers']
)
class LedgerEntryViewSet(CustomResponseModelViewSet):
    queryset = LedgerEntry.objects.all()
    serializer_class = LedgerEntrySerializer


class ReportsViewSet(viewsets.ViewSet):
    pagination_class = StandardResultsSetPagination
    @extend_schema(
        summary="Trial Balance Report",
        description="Shows debit, credit, and balance for each account based on journal entries.",
        tags=['Reports'],
        responses=TrialBalanceSerializer(many=True)
    )
    @decorators.action(detail=False, methods=['get'], url_path='trial-balance')

    def trial_balance(self, request):
        accounts = Account.objects.all()
        data = []
        for account in accounts:
            entries = JournalEntryLine.objects.filter(account=account)
            debit = entries.aggregate(Sum('debit'))['debit__sum'] or 0
            credit = entries.aggregate(Sum('credit'))['credit__sum'] or 0
            balance = debit - credit
            data.append({
                'account': account.name,
                'debit': debit,
                'credit': credit,
                'balance': balance
            })
        return Response(data=data)

    @extend_schema(
        summary="Profit and Loss Statement",
        description="Calculates revenue, expenses, and net profit or loss.",
        tags=['Reports'],
        responses=ProfitAndLossSerializer
    )
    @decorators.action(detail=False, methods=['get'], url_path='profit-and-loss')
    def profit_and_loss(self, request):
        revenue_accounts = Account.objects.filter(account_type='Revenue')
        expense_accounts = Account.objects.filter(account_type='Expense')

        revenue = JournalEntryLine.objects.filter(account__in=revenue_accounts).aggregate(Sum('credit'))['credit__sum'] or 0
        expenses = JournalEntryLine.objects.filter(account__in=expense_accounts).aggregate(Sum('debit'))['debit__sum'] or 0
        profit = revenue - expenses

        return Response(data={
            'revenue': revenue,
            'expenses': expenses,
            'profit_or_loss': profit
        })

    @extend_schema(
        summary="Accounts Receivable Summary",
        description="Shows total sales, payments received, and outstanding receivables.",
        tags=['Reports'],
        responses=AccountsReceivableSerializer
    )
    @decorators.action(detail=False, methods=['get'], url_path='accounts-receivable-summary')
    def accounts_receivable_summary(self, request):
        total_sales = SalesInvoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_payments = PaymentEntry.objects.filter(related_invoice__isnull=False).aggregate(Sum('amount'))['amount__sum'] or 0
        outstanding = total_sales - total_payments

        return Response(data={
            'total_sales': total_sales,
            'total_payments_received': total_payments,
            'outstanding_amount': outstanding
        })

    @extend_schema(
        summary="Gross Profit Report",
        description="Shows gross profit based on sales revenue and item cost.",
        tags=['Reports'],
        responses=GrossProfitSerializer
    )
    @decorators.action(detail=False, methods=['get'], url_path='gross-profit')
    def gross_profit(self, request):
        sales = SalesInvoiceItem.objects.annotate(
            cost=F('item__cost_price') * F('quantity'),
            revenue=F('rate') * F('quantity')
        )
        gross_profit = sales.aggregate(
            total_cost=Sum('cost'),
            total_revenue=Sum('revenue')
        )

        gross_profit_value = (gross_profit['total_revenue'] or 0) - (gross_profit['total_cost'] or 0)

        return Response(data={
            'total_cost': gross_profit['total_cost'],
            'total_revenue': gross_profit['total_revenue'],
            'gross_profit': gross_profit_value
        })

    @extend_schema(
        summary="Sales Trend Report",
        description="Returns sales totals over time filtered by range: 24h, 4d, 1w, 1m, 3m, 6m, 1y.",
        tags=['Reports'],
        parameters=[
            OpenApiParameter(name='range', description='Time range filter for trend', required=False, type=str,
                             enum=['24h', '4d', '1w', '1m', '3m', '6m', '1y']),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
            OpenApiParameter(name='page_size', description='Results per page', required=False, type=int),
        ],
        responses=PaginatedSalesTrendSerializer,
    )
    @decorators.action(detail=False, methods=['get'], url_path='sales-trend')
    def sales_trend(self, request):
        range_param = request.GET.get('range', '1m')
        current = timezone.now()

        ranges = {
            '24h': current - timedelta(hours=24),
            '4d': current - timedelta(days=4),
            '1w': current - timedelta(weeks=1),
            '1m': current - timedelta(days=30),
            '3m': current - timedelta(days=90),
            '6m': current - timedelta(days=180),
            '1y': current - timedelta(days=365),
        }

        if range_param not in ranges:
            return Response(message={
                "error": f"Invalid range '{range_param}'. Valid: 24h, 4d, 1w, 1m, 3m, 6m, 1y."
            }, status=400)

        start_date = ranges[range_param]

        if range_param in ['24h', '4d', '1w', '1m']:
            trunc = functions.TruncDay
        elif range_param in ['3m', '6m']:
            trunc = functions.TruncWeek
        else:
            trunc = functions.TruncMonth

        queryset = SalesInvoice.objects.filter(date__gte=start_date)
        trends = queryset.annotate(
            period=trunc('date')
        ).values('period').annotate(total_sales=Sum('total_amount')).order_by('period')
        # Paginate
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(trends, request)
        
        return Response(data={
            'total_count': paginator.page.paginator.count,
            'next_page': paginator.get_next_link(),
            'prev_page': paginator.get_previous_link(),
            'data': page
        })

    @extend_schema(
        summary="Purchase Trend Report",
        description="Returns purchase totals over time filtered by range: 24h, 4d, 1w, 1m, 3m, 6m, 1y.",
        tags=['Reports'],
        parameters=[
            OpenApiParameter(name='range', description='Time range filter for trend', required=False, type=str,
                             enum=['24h', '4d', '1w', '1m', '3m', '6m', '1y']),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
            OpenApiParameter(name='page_size', description='Results per page', required=False, type=int),
        ],
        responses=PaginatedPurchaseTrendSerializer,
    )
    @decorators.action(detail=False, methods=['get'], url_path='purchase-trend')
    def purchase_trend(self, request):
        range_param = request.GET.get('range', '1m')
        current = timezone.now()

        ranges = {
            '24h': current - timedelta(hours=24),
            '4d': current - timedelta(days=4),
            '1w': current - timedelta(weeks=1),
            '1m': current - timedelta(days=30),
            '3m': current - timedelta(days=90),
            '6m': current - timedelta(days=180),
            '1y': current - timedelta(days=365),
        }

        if range_param not in ranges:
            return Response(message={
                "error": f"Invalid range '{range_param}'. Valid: 24h, 4d, 1w, 1m, 3m, 6m, 1y."
            }, status=400)

        start_date = ranges[range_param]

        if range_param in ['24h', '4d', '1w', '1m']:
            trunc = functions.TruncDay
        elif range_param in ['3m', '6m']:
            trunc = functions.TruncWeek
        else:
            trunc = functions.TruncMonth

        queryset = PurchaseInvoice.objects.filter(date__gte=start_date)
        trends = queryset.annotate(
            period=trunc('date')
        ).values('period').annotate(total_purchases=Sum('total_amount')).order_by('period')
        
        
        # Paginate
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(trends, request)
        
        return Response(data={
            'total_count': paginator.page.paginator.count,
            'next_page': paginator.get_next_link(),
            'prev_page': paginator.get_previous_link(),
            'data': page
        })
    
