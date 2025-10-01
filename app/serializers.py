from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'due_date']

class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    members_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=User.objects.all(), source='members')
    tasks = TaskSerializer(many=True, read_only=True, source='tarefas')
    class Meta:
        model = Project
        fields = ['id', 'title', 'members', 'members_ids', 'tasks']
