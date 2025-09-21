from django.contrib import admin
from .models import Project, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('members',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'project', 'assignee', 'created_at')
    list_filter = ('status', 'due_date', 'project', 'assignee')
    search_fields = ('title', 'description')
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
