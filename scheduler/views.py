# scheduler/views.py

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, View, UpdateView, ListView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from .models import Task
from .forms import TaskForm

class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('scheduler:login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

class DeleteUserView(LoginRequiredMixin, DeleteView):
    template_name = 'registration/delete_user.html'
    success_url = reverse_lazy('scheduler:logout')

class TimeManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'scheduler/time_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user).order_by('-priority')
        total_time = TaskListView.calculate_total_time(tasks)
        context['tasks'] = tasks
        context['total_time'] = total_time
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'scheduler/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-priority']

    @staticmethod
    def calculate_total_time(tasks):
        total_time = tasks.aggregate(Sum('usage_time'))['usage_time__sum']
        if total_time and isinstance(total_time, timedelta):
            return TaskListView.format_timedelta(total_time)
        return "0:00"

    def get_queryset(self):
        tasks = super().get_queryset()
        for i in range(len(tasks)):
            task = tasks[i]
            task.remaining_time = self.calculate_remaining_time(task.usage_time)

            if i < len(tasks) - 1:
                next_task_start_time = tasks[i + 1].usage_time
                time_until_next_task = next_task_start_time - task.usage_time
                task.time_until_next_task = TaskListView.format_timedelta(time_until_next_task)
            else:
                task.time_until_next_task = None

        return tasks

    @staticmethod
    def calculate_remaining_time(task_usage_time):
        remaining_time_minutes = 24 * 60 - task_usage_time.total_seconds() // 60
        remaining_hours, remaining_minutes = divmod(remaining_time_minutes, 60)
        remaining_time_formatted = "{:02}:{:02}".format(int(remaining_hours), int(remaining_minutes))
        return remaining_time_formatted

    @staticmethod
    def format_timedelta(timedelta):
        total_minutes = int(timedelta.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return "{:02}:{:02}".format(hours, minutes)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('scheduler:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'usage_time' in form.cleaned_data:
            form.instance.deadline = timezone.now() + form.cleaned_data['usage_time']
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'scheduler/task_confirm_delete.html'
    success_url = reverse_lazy('scheduler:task_list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('scheduler:task_list')

class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        task.completed = not task.completed
        task.save()
        return redirect('scheduler:task_list')
