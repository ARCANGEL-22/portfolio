# views.py - REDLINE Django REST Framework
# ViewSets for the project management API.

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count, Q
from django.utils import timezone
from .models import Project, WorkOrder, Milestone, User
from .serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    WorkOrderSerializer,
    MilestoneSerializer,
)
from .permissions import IsPMOrAdmin, IsOwnerOrAdmin


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD + custom actions for fiber construction projects."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'county', 'state', 'description']
    ordering_fields = ['created_at', 'target_completion', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Project.objects.select_related('project_manager').prefetch_related(
            'milestones', 'work_orders__assigned_to'
        )
        user = self.request.user

        # Contractors only see projects they have work orders on
        if user.role == User.Role.CONTRACTOR:
            qs = qs.filter(work_orders__assigned_to=user).distinct()

        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectDetailSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsPMOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(project_manager=self.request.user)

    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """Return a dashboard summary for a single project."""
        project = self.get_object()
        work_orders = project.work_orders.all()

        status_counts = dict(
            work_orders.values('status').annotate(count=Count('id')).values_list('status', 'count')
        )

        overdue = work_orders.filter(
            due_date__lt=timezone.now().date(),
            status__in=['unassigned', 'assigned', 'in_progress']
        ).count()

        return Response({
            'project_id': str(project.id),
            'name': project.name,
            'status': project.status,
            'completion_pct': project.completion_pct,
            'work_order_status_counts': status_counts,
            'overdue_work_orders': overdue,
            'milestone_count': project.milestones.count(),
            'milestones_complete': project.milestones.filter(status='complete').count(),
        })

    @action(detail=True, methods=['patch'], url_path='status', permission_classes=[IsAuthenticated, IsPMOrAdmin])
    def update_status(self, request, pk=None):
        """Update project status with validation."""
        project = self.get_object()
        new_status = request.data.get('status')

        valid_statuses = [s.value for s in Project.Status]
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        project.status = new_status
        project.save(update_fields=['status', 'updated_at'])
        return Response({'status': new_status}, status=status.HTTP_200_OK)


class WorkOrderViewSet(viewsets.ModelViewSet):
    """CRUD for work orders with contractor-scoped filtering."""

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkOrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = WorkOrder.objects.select_related('project', 'assigned_to')
        user = self.request.user

        if user.role == User.Role.CONTRACTOR:
            qs = qs.filter(assigned_to=user)

        # Allow filtering by project
        project_id = self.request.query_params.get('project')
        if project_id:
            qs = qs.filter(project_id=project_id)

        # Allow filtering by status
        status_param = self.request.query_params.get('status')
        if status_param:
            qs = qs.filter(status=status_param)

        return qs

    def get_permissions(self):
        if self.action in ('create', 'destroy'):
            return [IsAuthenticated(), IsPMOrAdmin()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['patch'], url_path='assign')
    def assign(self, request, pk=None):
        """Assign a work order to a contractor."""
        if not request.user.is_pm:
            return Response(
                {'error': 'Only PMs can assign work orders.'},
                status=status.HTTP_403_FORBIDDEN
            )

        work_order = self.get_object()
        contractor_id = request.data.get('contractor_id')

        try:
            contractor = User.objects.get(id=contractor_id, role=User.Role.CONTRACTOR)
        except User.DoesNotExist:
            return Response(
                {'error': 'Contractor not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        work_order.assigned_to = contractor
        work_order.status = WorkOrder.Status.ASSIGNED
        work_order.save(update_fields=['assigned_to', 'status', 'updated_at'])

        return Response(WorkOrderSerializer(work_order).data)
