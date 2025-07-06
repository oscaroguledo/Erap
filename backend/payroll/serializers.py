from rest_framework import serializers
from .models import (
    SalaryComponent, PayrollPeriod, IncomeTaxSlab, SalaryStructure,
    SalaryStructureComponent, SalarySlip, PayrollSettings
)
from hr.serializers import EmployeeSerializer  # Assuming your Employee serializer is here

class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = '__all__'

class PayrollPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = '__all__'

class IncomeTaxSlabSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTaxSlab
        fields = '__all__'

class SalaryStructureComponentSerializer(serializers.ModelSerializer):
    salary_component = SalaryComponentSerializer(read_only=True)
    salary_component_id = serializers.PrimaryKeyRelatedField(
        queryset=SalaryComponent.objects.all(), source='salary_component', write_only=True)

    class Meta:
        model = SalaryStructureComponent
        fields = ['id', 'salary_component', 'salary_component_id', 'amount']

class SalaryStructureSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSerializer.Meta.model.objects.all(),
        source='employee', write_only=True
    )
    components = SalaryStructureComponentSerializer(
        source='salarystructurecomponent_set', many=True, read_only=True
    )

    class Meta:
        model = SalaryStructure
        fields = ['id', 'employee', 'employee_id', 'effective_from', 'effective_to', 'components']

class SalarySlipSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeSerializer.Meta.model.objects.all(),
        source='employee', write_only=True
    )
    payroll_period = PayrollPeriodSerializer(read_only=True)
    payroll_period_id = serializers.PrimaryKeyRelatedField(
        queryset=PayrollPeriod.objects.all(),
        source='payroll_period', write_only=True
    )
    salary_structure = SalaryStructureSerializer(read_only=True)
    salary_structure_id = serializers.PrimaryKeyRelatedField(
        queryset=SalaryStructure.objects.all(),
        source='salary_structure', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = SalarySlip
        fields = [
            'id', 'employee', 'employee_id',
            'payroll_period', 'payroll_period_id',
            'salary_structure', 'salary_structure_id',
            'total_earnings', 'total_deductions', 'net_salary', 'generated_on'
        ]
        read_only_fields = ['generated_on']

class PayrollSettingsSerializer(serializers.ModelSerializer):
    tax_slab = IncomeTaxSlabSerializer(read_only=True)
    tax_slab_id = serializers.PrimaryKeyRelatedField(
        queryset=IncomeTaxSlab.objects.all(),
        source='tax_slab', write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = PayrollSettings
        fields = ['id', 'tax_slab', 'tax_slab_id', 'fiscal_year_start', 'fiscal_year_end']
