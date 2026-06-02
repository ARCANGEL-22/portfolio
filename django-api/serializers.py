# serializers.py - REDLINE Django REST Framework
# DRF serializers for the project and work order API.

from rest_framework import serializers
from .models import User, Project, WorkOrder, Milestone


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight user representation for nested use in other serializers."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'company']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class MilestoneSerializer(serializers.ModelSerializer):
    """Full milestone serializer with status display."""

    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Milestone
        fields = [
            'id', 'name', 'description', 'status', 'status_display',
            'due_date', 'completed_at', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class WorkOrderSerializer(serializers.ModelSerializer):
    """Work order with nested contractor info and computed fields."""

    assigned_to = UserSummarySerializer(read_only=True)
    assigned_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    work_type_display = serializers.CharField(source='get_work_type_display', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = [
            'id', 'project', 'title', 'description',
            'work_type', 'work_type_display',
            'status', 'status_display',
            'assigned_to', 'assigned_to_id',
            'estimated_hours', 'actual_hours',
            'due_date', 'completed_at',
            'is_overdue', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def get_is_overdue(self, obj):
        from django.utils import timezone
        if obj.due_date and obj.status not in ('complete', 'cancelled'):
            return obj.due_date < timezone.now().date()
        return False

    def validate_assigned_to_id(self, value):
        if value and not User.objects.filter(id=value, role=User.Role.CONTRACTOR).exists():
            raise serializers.ValidationError('Assigned user must be a contractor.')
        return value

    def update(self, instance, validated_data):
        from django.utils import timezone
        assigned_to_id = validated_data.pop('assigned_to_id', ...)
        if assigned_to_id is not ...:
            instance.assigned_to_id = assigned_to_id

        # Auto-stamp completion time
        new_status = validated_data.get('status', instance.status)
        if new_status == 'complete' and instance.status != 'complete':
            instance.completed_at = timezone.now()
        elif new_status != 'complete':
            instance.completed_at = None

        return super().update(instance, validated_data)


class ProjectListSerializer(serializers.ModelSerializer):
    """Compact project representation for list endpoints."""

    project_manager = UserSummarySerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    completion_pct = serializers.IntegerField(read_only=True)
    work_order_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'status', 'status_display',
            'project_manager', 'state', 'county',
            'total_miles', 'completion_pct', 'work_order_count',
            'start_date', 'target_completion', 'updated_at',
        ]

    def get_work_order_count(self, obj):
        return obj.work_orders.count()


class ProjectDetailSerializer(ProjectListSerializer):
    """Full project detail with nested milestones and work orders."""

    milestones = MilestoneSerializer(many=True, read_only=True)
    work_orders = WorkOrderSerializer(many=True, read_only=True)
    project_manager_id = serializers.UUIDField(write_only=True, required=False)

    class Meta(ProjectListSerializer.Meta):
        fields = ProjectListSerializer.Meta.fields + [
            'description', 'budget', 'milestones', 'work_orders',
            'project_manager_id', 'created_at',
        ]
