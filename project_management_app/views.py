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
    @action(detail=True,methods=["PATCH"])
    def update_status(self,request,pk=None):
        task=self.get_object()
        if request.user.role=="member":
            task.status=request.data.get('status',task.status)
            task.save()
            return Response({'status':'updated'})
        return Response({'error':"Not Allowd"},status=403)

# Create your views here.
