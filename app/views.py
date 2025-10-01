from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from .forms import ProjectForm, TaskForm, SignUpForm
from django.db.models import Q

from django.contrib.auth.models import User
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer, UserSerializer
from .permissions import IdProjectMember


def login_view(request):
    # Se o usuário já está logado, redireciona para o dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Verifica se é o primeiro acesso (não há usuários cadastrados)
    if not User.objects.exists():
        messages.info(request, 'Bem-vindo! Este parece ser o primeiro acesso. Crie sua conta para começar.')
        return redirect('signup')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redireciona para a página solicitada ou dashboard
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Você foi desconectado com sucesso.')
    return redirect('login')


@login_required
def dashboard_view(request):
    # Obter projetos do usuário
    projects = Project.objects.filter(members=request.user).prefetch_related('tarefas')
    
    # Obter tarefas do usuário
    tasks = Task.objects.filter(project__in=projects).select_related('project', 'assignee')
    
    # Estatísticas
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(status='Pending').count()
    in_progress_tasks = tasks.filter(status='In Progress').count()
    completed_tasks = tasks.filter(status='Completed').count()
    
    context = {
        'projects': projects,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }
    
    return render(request, 'dashboard.html', context)



@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, project__members=request.user)
        new_status = request.POST.get('status')
        
        # Lista de status válidos
        valid_statuses = ['Pending', 'In Progress', 'Completed']
        
        if new_status in valid_statuses:
            task.status = new_status
            task.save()
            return JsonResponse({
                'success': True, 
                'status': new_status,
                'message': f'Status atualizado para {new_status}'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'Status inválido'
            })
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'})



@login_required
def projects_view(request):
    projects = Project.objects.filter(members=request.user).prefetch_related('tarefas', 'members')
    
    # Estatísticas por projeto
    project_stats = []
    for project in projects:
        tasks = project.tarefas.all()
        stats = {
            'project': project,
            'total_tasks': tasks.count(),
            'pending_tasks': tasks.filter(status='Pending').count(),
            'in_progress_tasks': tasks.filter(status='In Progress').count(),
            'completed_tasks': tasks.filter(status='Completed').count(),
        }
        project_stats.append(stats)
    
    context = {
        'project_stats': project_stats,
        'projects': projects,
    }
    
    return render(request, 'projects.html', context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        
        # Atualizar dados básicos
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Verificar se quer alterar a senha
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    messages.success(request, 'Senha alterada com sucesso! Faça login novamente.')
                    user.save()
                    logout(request)
                    return redirect('login')
                else:
                    messages.error(request, 'As senhas não coincidem.')
                    return render(request, 'profile.html')
            else:
                messages.error(request, 'Senha atual incorreta.')
                return render(request, 'profile.html')
        
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('profile')
    
    return render(request, 'profile.html')


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
        return self.queryset.filter(project__members=user)

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Se o usuário já está logado, redireciona para o dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso! Agora você pode fazer login.')
        return response

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'create_project.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.members.add(self.request.user)
        return response

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project_confirm_delete.html'
    success_url = reverse_lazy('projects')

    def get_queryset(self):
        return super().get_queryset().filter(members=self.request.user)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return super().get_queryset().filter(project__members=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarefa excluída com sucesso!')
        return super().form_valid(form)
