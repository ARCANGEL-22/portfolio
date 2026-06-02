# models.py - REDLINE Django REST Framework
# Contractor and project management data models.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid


class User(AbstractUser):
    """Extended user model with role-based access control."""

    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        PROJECT_MANAGER = 'pm', _('Project Manager')
        CONTRACTOR = 'contractor', _('Contractor')
        VIEWER = 'viewer', _('Viewer')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_pm(self):
        return self.role in (self.Role.ADMIN, self.Role.PROJECT_MANAGER)


class Project(models.Model):
    """A fiber construction project with geographic scope."""

    class Status(models.TextChoices):
        PLANNING = 'planning', _('Planning')
        ACTIVE = 'active', _('Active')
        ON_HOLD = 'on_hold', _('On Hold')
        COMPLETE = 'complete', _('Complete')
        CANCELLED = 'cancelled', _('Cancelled')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNING)
    project_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='managed_projects'
    )
    state = models.CharField(max_length=2)  # US state abbreviation
    county = models.CharField(max_length=100)
    total_miles = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    target_completion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

    @property
    def completion_pct(self):
        """Calculate completion percentage based on milestones."""
        total = self.milestones.count()
        if total == 0:
            return 0
        done = self.milestones.filter(status=Milestone.Status.COMPLETE).count()
        return round((done / total) * 100)


class WorkOrder(models.Model):
    """A discrete unit of construction work assigned to a contractor."""

    class Status(models.TextChoices):
        UNASSIGNED = 'unassigned', _('Unassigned')
        ASSIGNED = 'assigned', _('Assigned')
        IN_PROGRESS = 'in_progress', _('In Progress')
        PENDING_QC = 'pending_qc', _('Pending QC')
        COMPLETE = 'complete', _('Complete')
        REJECTED = 'rejected', _('Rejected')

    class WorkType(models.TextChoices):
        AERIAL = 'aerial', _('Aerial')
        UNDERGROUND = 'underground', _('Underground')
        SPLICING = 'splicing', _('Splicing')
        MAKE_READY = 'make_ready', _('Make-Ready')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_orders')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders'
    )
    work_type = models.CharField(max_length=20, choices=WorkType.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UNASSIGNED)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'work_orders'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['assigned_to', 'status']),
        ]

    def __str__(self):
        return f'{self.title} [{self.get_status_display()}]'


class Milestone(models.Model):
    """A project milestone tracking major deliverables."""

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        IN_PROGRESS = 'in_progress', _('In Progress')
        COMPLETE = 'complete', _('Complete')
        OVERDUE = 'overdue', _('Overdue')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'milestones'
        ordering = ['due_date']

    def __str__(self):
        return f'{self.project.name} - {self.name}'
