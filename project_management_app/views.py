from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsAdminPermissionOnly, IsMemberOrAdminOnly

class ProjectViewset(viewsets.ModelViewSet):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=[IsAdminPermissionOnly]
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
class TaskViewset(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    permission_classes=[IsMemberOrAdminOnly]
    pagination_class = PageNumberPagination  
    def get_queryset(self):
        if self.request.user.role == "member":
            return Task.objects.filter(assigned_to=self.request.user)
        return Task.objects.all()
    @action(detail=True, methods=["PATCH"])
    def update_status(self, request, pk=None):
        """Allow only assigned members to update the status of their tasks."""
        task = self.get_object()

        # Ensure user is assigned to this task
        if task.assigned_to != request.user:
            return Response({'error': "You can only update your assigned tasks."}, status=403)

        # Validate new status
        new_status = request.data.get('status')
        valid_statuses = dict(Task.STATUS_CHOICES)

        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status value'}, status=400)

        # Update status
        task.status = new_status
        task.save(update_fields=['status'])

        return Response({'status': 'updated', 'new_status': new_status})

# Create your views here.
