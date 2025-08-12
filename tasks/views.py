# tasks/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from .models import Project, Task
from django.db.models import Q
from .serializers import ProjectSerializer, TaskSerializer
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .tasks import send_assignment_email_task
from rest_framework import generics
from .serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [] 
    
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            Q(owner=user) | Q(tasks__assigned_to=user)
        ).distinct().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status","priority","due_date","project"]
    ordering_fields = ["priority","due_date"]
    
    def get_queryset(self):
        # Only tasks belonging to current user's projects
        return Task.objects.filter(project__owner=self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        # attach created_by
        task = serializer.save(created_by=self.request.user)
        if task.assigned_to:
            send_assignment_email_task.delay(task.id, "assigned")
    
    def perform_update(self, serializer):
        instance = serializer.instance
        old_status = instance.status
        old_assigned = instance.assigned_to
        task = serializer.save()
        if task.assigned_to and (old_assigned != task.assigned_to):
            send_assignment_email_task.delay(task.id, "assigned")
        if old_status != task.status:
            send_assignment_email_task.delay(task.id, "status_changed")
