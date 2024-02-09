# scheduler/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, View, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
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
        tasks = Task.objects.filter(user=self.request.user).order_by('start_time')
        total_time = TaskListView.calculate_remaining_time(tasks)
        context['tasks'] = tasks
        context['total_time'] = total_time
        return context

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'scheduler/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        tasks = super().get_queryset()

        # 開始時間に基づいて昇順にソート
        tasks = tasks.order_by('start_time')

        for i in range(len(tasks)):
            task = tasks[i]
            task.remaining_time = TaskListView.calculate_remaining_time(task.usage_time)

            if i < len(tasks) - 1:
                next_task_start_time = tasks[i + 1].start_time
                time_until_next_task = next_task_start_time - task.start_time
                task.time_until_next_task = TaskListView.format_timedelta(time_until_next_task)
            else:
                task.time_until_next_task = None

            # 開始時間のフォーマットを行う
            task.start_time_formatted = self.format_datetime(task.start_time)
            # 終了時間のフォーマットを行う
            task.end_time_formatted = self.format_datetime(task.deadline)

        return tasks

    @staticmethod
    def calculate_remaining_time(task_usage_time):
        if isinstance(task_usage_time, timedelta):
            remaining_time_minutes = 24 * 60 - task_usage_time.total_seconds() // 60
            remaining_hours, remaining_minutes = divmod(remaining_time_minutes, 60)
            remaining_time_formatted = "{:02}:{:02}".format(int(remaining_hours), int(remaining_minutes))
            return remaining_time_formatted
        else:
            pass

    @staticmethod
    def format_timedelta(timedelta):
        total_minutes = int(timedelta.total_seconds() // 60)
        hours, minutes = divmod(total_minutes, 60)
        return "{:02}:{:02}".format(hours, minutes)

    @staticmethod
    def format_datetime(datetime_value):
        return datetime_value.strftime("%Y年%m月%d日 %H:%M") if datetime_value else "-"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'scheduler/task_form.html'
    success_url = reverse_lazy('scheduler:task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        # 開始時間と終了時間の取得
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')
        if start_time and end_time:
            form.instance.usage_time = end_time - start_time
            form.instance.deadline = end_time

        # 親クラスの form_valid メソッドを呼び出し、新しいタスクを保存
        response = super().form_valid(form)

        # タスクリストのビューにリダイレクト
        return redirect('scheduler:task_list')

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
