from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProjectViewSet, TaskViewSet,
    login_view, logout_view, dashboard_view,
    update_task_status, TaskDeleteView,
    projects_view, ProjectCreateView, ProjectDeleteView,
    TaskCreateView, profile_view, SignUpView
)


router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Web views
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Tasks
    path('tasks/create/', TaskCreateView.as_view(), name='create_task'),
    path('task/<int:task_id>/update-status/', update_task_status, name='update_task_status'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='delete_task'),
    
    # Projects
    path('projects/', projects_view, name='projects'),
    path('projects/create/', ProjectCreateView.as_view(), name='create_project'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete_project'),
    
    # Profile
    path('profile/', profile_view, name='profile'),
    
    # API routes
    path('api/', include(router.urls)),

   
]