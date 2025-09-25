from rest_framework import permissions
from .models import Project, Task 

class IdProjectMember(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if isinstance(obj, Project):
            return request.user in obj.members.all()
        
        if isinstance(obj, Task):
            return request.user in obj.project.members.all()
        
        return False