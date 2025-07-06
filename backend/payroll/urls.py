from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalaryComponentViewSet, PayrollPeriodViewSet, IncomeTaxSlabViewSet,
    SalaryStructureViewSet, SalaryStructureComponentViewSet, SalarySlipViewSet,
    PayrollSettingsViewSet
)

router = DefaultRouter()

router.register(r'salary-components', SalaryComponentViewSet, basename='salarycomponent')
router.register(r'payroll-periods', PayrollPeriodViewSet, basename='payrollperiod')
router.register(r'income-tax-slabs', IncomeTaxSlabViewSet, basename='incometaxslab')
router.register(r'salary-structures', SalaryStructureViewSet, basename='salarystructure')
router.register(r'salary-structure-components', SalaryStructureComponentViewSet, basename='salarystructurecomponent')
router.register(r'salary-slips', SalarySlipViewSet, basename='salaryslip')
router.register(r'payroll-settings', PayrollSettingsViewSet, basename='payrollsettings')

urlpatterns = [
    path('', include(router.urls)),
]