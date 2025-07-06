from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet, BranchViewSet, DepartmentViewSet, DesignationViewSet,
    EmployeeGradeViewSet, EmployeeViewSet, HRSettingsViewSet, EmployeeAdvanceViewSet,
    ExpenseClaimViewSet, AttendanceViewSet, EmployeeCheckinViewSet,
    LeaveTypeViewSet, LeaveAllocationViewSet, LeaveApplicationViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'designations', DesignationViewSet, basename='designation')
router.register(r'employee-grades', EmployeeGradeViewSet, basename='employeegrade')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'hr-settings', HRSettingsViewSet, basename='hrsettings')
router.register(r'employee-advances', EmployeeAdvanceViewSet, basename='employeeadvance')
router.register(r'expense-claims', ExpenseClaimViewSet, basename='expenseclaim')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'employee-checkins', EmployeeCheckinViewSet, basename='employeecheckin')
router.register(r'leave-types', LeaveTypeViewSet, basename='leavetype')
router.register(r'leave-allocations', LeaveAllocationViewSet, basename='leaveallocation')
router.register(r'leave-applications', LeaveApplicationViewSet, basename='leaveapplication')

urlpatterns = [
    path('', include(router.urls)),
]
