from django.db import models
from django.contrib.auth.models import User

class Project (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task (models.Model):
    
    class Status(models.TextChoices):
        PENDING = "Pending", "Pendente"
        IN_PROGRESS = "In Progress", "Em progresso"
        COMPLETED = "Completed", "Concluído"

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    due_date = models.DateField(blank=True, null=True)

    project  = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='Projeto')
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='task',
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"