from rest_framework import viewsets, status, pagination

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import (
    Company, Branch, Department, Designation, EmployeeGrade,
    Employee, HRSettings, EmployeeAdvance, ExpenseClaim,
    Attendance, EmployeeCheckin, LeaveType, LeaveAllocation, LeaveApplication
)

from .serializers import (
    CompanySerializer, BranchSerializer, DepartmentSerializer,
    DesignationSerializer, EmployeeGradeSerializer, EmployeeSerializer,
    HRSettingsSerializer, EmployeeAdvanceSerializer, ExpenseClaimSerializer,
    AttendanceSerializer, EmployeeCheckinSerializer, LeaveTypeSerializer,
    LeaveAllocationSerializer, LeaveApplicationSerializer
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
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Manage companies",
    description="Create, update, delete and list company records.",
    tags=["Company"]
)
class CompanyViewSet(CustomResponseModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

@extend_schema(
    summary="Manage branches",
    description="Operations for company branches including create, update, list and delete.",
    tags=["Branch"]
)
class BranchViewSet(CustomResponseModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

@extend_schema(
    summary="Manage departments",
    description="Handle organizational departments including their details and hierarchy.",
    tags=["Department"]
)
class DepartmentViewSet(CustomResponseModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

@extend_schema(
    summary="Manage designations",
    description="Create, update, list and delete employee designations.",
    tags=["Designation"]
)
class DesignationViewSet(CustomResponseModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

@extend_schema(
    summary="Manage employee grades",
    description="Handle different grades of employees within the organization.",
    tags=["Employee Grade"]
)
class EmployeeGradeViewSet(CustomResponseModelViewSet):
    queryset = EmployeeGrade.objects.all()
    serializer_class = EmployeeGradeSerializer

@extend_schema(
    summary="Manage employees",
    description="Create, retrieve, update, delete and list employees.",
    tags=["Employee"]
)
class EmployeeViewSet(CustomResponseModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

@extend_schema(
    summary="Manage HR settings",
    description="Configure human resource related settings.",
    tags=["HR Settings"]
)
class HRSettingsViewSet(CustomResponseModelViewSet):
    queryset = HRSettings.objects.all()
    serializer_class = HRSettingsSerializer

@extend_schema(
    summary="Manage employee advances",
    description="Operations related to employee advance payments.",
    tags=["Employee Advance"]
)
class EmployeeAdvanceViewSet(CustomResponseModelViewSet):
    queryset = EmployeeAdvance.objects.all()
    serializer_class = EmployeeAdvanceSerializer

@extend_schema(
    summary="Manage expense claims",
    description="Handle employee expense claims submission and approval.",
    tags=["Expense Claim"]
)
class ExpenseClaimViewSet(CustomResponseModelViewSet):
    queryset = ExpenseClaim.objects.all()
    serializer_class = ExpenseClaimSerializer

@extend_schema(
    summary="Manage attendance",
    description="Track and manage employee attendance records.",
    tags=["Attendance"]
)
class AttendanceViewSet(CustomResponseModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

@extend_schema(
    summary="Manage employee check-ins",
    description="Track employee check-in and check-out timestamps.",
    tags=["Employee Check-in"]
)
class EmployeeCheckinViewSet(CustomResponseModelViewSet):
    queryset = EmployeeCheckin.objects.all()
    serializer_class = EmployeeCheckinSerializer

@extend_schema(
    summary="Manage leave types",
    description="Create and manage types of leaves available.",
    tags=["Leave Type"]
)
class LeaveTypeViewSet(CustomResponseModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

@extend_schema(
    summary="Manage leave allocations",
    description="Allocate leaves to employees and manage quotas.",
    tags=["Leave Allocation"]
)
class LeaveAllocationViewSet(CustomResponseModelViewSet):
    queryset = LeaveAllocation.objects.all()
    serializer_class = LeaveAllocationSerializer

@extend_schema(
    summary="Manage leave applications",
    description="Handle employee leave requests and approval workflows.",
    tags=["Leave Application"]
)
class LeaveApplicationViewSet(CustomResponseModelViewSet):
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializer
