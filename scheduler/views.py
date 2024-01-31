from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView, TemplateView, View, UpdateView, ListView, DeleteView
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from datetime import timedelta

from .models import Task, List
from .forms import TaskForm, ListForm

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
        total_time, remaining_time = self.calculate_total_and_remaining_time(tasks)
        context['tasks'] = tasks
        context['total_time'] = total_time
        context['remaining_time'] = remaining_time

        list_instance = List.objects.filter(user=self.request.user).first()
        if list_instance:
            list_edit_link = reverse('scheduler:list_edit', args=[list_instance.pk])
            context['list_edit_link'] = list_edit_link

        task_list_link = reverse('scheduler:task_list')
        context['task_list_link'] = task_list_link

        return context

    @staticmethod
    def calculate_total_and_remaining_time(tasks):
        total_time = tasks.aggregate(Sum('usage_time'))['usage_time__sum']
        remaining_time = timedelta(minutes=24*60) - total_time if total_time else timedelta(minutes=24*60)
        
        if total_time and isinstance(total_time, timedelta):
            total_time = TimeManagementView.format_timedelta(total_time)
            remaining_time = TimeManagementView.format_timedelta(remaining_time)

        return total_time, remaining_time

    @staticmethod
    def format_timedelta(timedelta):
        total_minutes = int(timedelta.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return "{:02}:{:02}".format(hours, minutes)

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

    def delete(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseRedirect(self.get_success_url())
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('scheduler:task_list')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('scheduler:task_list')

class TaskToggleStatusView(LoginRequiredMixin, View):
    @require_POST
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs['pk'])
        task.completed = not task.completed
        task.save()

        list_instance = task.list
        if list_instance:
            list_overview_url = reverse('scheduler:list_list')
            return redirect(list_overview_url)
        else:
            return redirect('scheduler:task_list')

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    form_class = ListForm
    template_name = 'scheduler/list_form.html'
    success_url = reverse_lazy('scheduler:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListEditView(LoginRequiredMixin, UpdateView):
    model = List
    form_class = ListForm
    template_name = 'scheduler/list_form.html'
    success_url = reverse_lazy('scheduler:task_list')

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = 'scheduler/list_list.html'
    context_object_name = 'lists'

    def get_queryset(self):
        return List.objects.filter(user=self.request.user)

class AddTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/add_task.html'
    success_url = reverse_lazy('scheduler:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        if 'usage_time' in form.cleaned_data:
            form.instance.deadline = timezone.now() + form.cleaned_data['usage_time']
        return super().form_valid(form)

@require_POST
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully'})

class ListToggleStatusView(LoginRequiredMixin, View):
    @require_POST
    def post(self, request, *args, **kwargs):
        list_instance = List.objects.get(pk=kwargs['pk'])
        list_instance.completed = not list_instance.completed
        list_instance.save()
        return redirect('scheduler:list_list')

