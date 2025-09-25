from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer
from .permissions import IdProjectMember


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().prefetch_related('members', 'tarefas')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IdProjectMember]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(members=user)

    def perform_create(self, serializer):
        project = serializer.save()
        project.members.add(self.request.user)
        project.save()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('project', 'assignee')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IdProjectMember]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(project__in=user.projetos.all())
