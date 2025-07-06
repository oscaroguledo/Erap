from rest_framework import viewsets, status, pagination
from drf_spectacular.utils import extend_schema
from drf_spectacular.openapi import AutoSchema
from backend.utils.response import Response
from .models import (
    SalaryComponent, PayrollPeriod, IncomeTaxSlab, SalaryStructure,
    SalaryStructureComponent, SalarySlip, PayrollSettings
)
from .serializers import (
    SalaryComponentSerializer, PayrollPeriodSerializer, IncomeTaxSlabSerializer,
    SalaryStructureSerializer, SalaryStructureComponentSerializer,
    SalarySlipSerializer, PayrollSettingsSerializer
)

class CustomSchema(AutoSchema):
    pass

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Manage salary components",
    description="Create, retrieve, update, delete and list salary components.",
    tags=["Payroll - Salary Component"]
)
class SalaryComponentViewSet(CustomResponseModelViewSet):
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer


@extend_schema(
    summary="Manage payroll periods",
    description="Create and manage payroll periods for salary processing.",
    tags=["Payroll - Payroll Period"]
)
class PayrollPeriodViewSet(CustomResponseModelViewSet):
    queryset = PayrollPeriod.objects.all()
    serializer_class = PayrollPeriodSerializer


@extend_schema(
    summary="Manage income tax slabs",
    description="Create and update income tax slabs used for payroll tax calculations.",
    tags=["Payroll - Income Tax Slab"]
)
class IncomeTaxSlabViewSet(CustomResponseModelViewSet):
    queryset = IncomeTaxSlab.objects.all()
    serializer_class = IncomeTaxSlabSerializer


@extend_schema(
    summary="Manage salary structures",
    description="Assign salary components to employees with effective dates.",
    tags=["Payroll - Salary Structure"]
)
class SalaryStructureViewSet(CustomResponseModelViewSet):
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer


@extend_schema(
    summary="Manage salary structure components",
    description="Details of components within a salary structure and their amounts.",
    tags=["Payroll - Salary Structure Component"]
)
class SalaryStructureComponentViewSet(CustomResponseModelViewSet):
    queryset = SalaryStructureComponent.objects.all()
    serializer_class = SalaryStructureComponentSerializer


@extend_schema(
    summary="Manage salary slips",
    description="Generate and retrieve salary slips for employees per payroll period.",
    tags=["Payroll - Salary Slip"]
)
class SalarySlipViewSet(CustomResponseModelViewSet):
    queryset = SalarySlip.objects.all()
    serializer_class = SalarySlipSerializer


@extend_schema(
    summary="Manage payroll settings",
    description="Configure global payroll settings such as fiscal year and tax slab.",
    tags=["Payroll - Settings"]
)
class PayrollSettingsViewSet(CustomResponseModelViewSet):
    queryset = PayrollSettings.objects.all()
    serializer_class = PayrollSettingsSerializer
