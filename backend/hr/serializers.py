from rest_framework import serializers
from .models import Company, Branch, Department, Designation, EmployeeGrade, EmployeeAdvance, ExpenseClaim,Employee,HRSettings,Attendance, EmployeeCheckin,LeaveType, LeaveAllocation, LeaveApplication
from accounting.serializers import CompanySerializer


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'

class EmployeeGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeGrade
        fields = '__all__'



class HRSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HRSettings
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    branch = BranchSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    designation = DesignationSerializer(read_only=True)
    grade = EmployeeGradeSerializer(read_only=True)

    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), source='branch', write_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True)
    designation_id = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(), source='designation', write_only=True)
    grade_id = serializers.PrimaryKeyRelatedField(
        queryset=EmployeeGrade.objects.all(), source='grade', write_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeAdvanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    class Meta:
        model = EmployeeAdvance
        fields = '__all__'

class ExpenseClaimSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    advance = EmployeeAdvanceSerializer(read_only=True)
    advance_id = serializers.PrimaryKeyRelatedField(queryset=EmployeeAdvance.objects.all(), source='advance', write_only=True, allow_null=True, required=False)

    class Meta:
        model = ExpenseClaim
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'

class EmployeeCheckinSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    class Meta:
        model = EmployeeCheckin
        fields = '__all__'

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveAllocationSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    leave_type = LeaveTypeSerializer(read_only=True)
    leave_type_id = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all(), source='leave_type', write_only=True)

    class Meta:
        model = LeaveAllocation
        fields = '__all__'

class LeaveApplicationSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), source='employee', write_only=True)

    leave_type = LeaveTypeSerializer(read_only=True)
    leave_type_id = serializers.PrimaryKeyRelatedField(queryset=LeaveType.objects.all(), source='leave_type', write_only=True)

    class Meta:
        model = LeaveApplication
        fields = '__all__'