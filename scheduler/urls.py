from django.urls import path
from .views import (
    SignUpView, CustomLoginView, CustomLogoutView,
    DeleteUserView, TimeManagementView, TaskListView,
    TaskCreateView, TaskDeleteView, TaskUpdateView, TaskToggleStatusView,
    ListCreateView, ListEditView, ListListView, AddTaskView, delete_task, ListToggleStatusView,
)

app_name = 'scheduler'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('delete_user/', DeleteUserView.as_view(), name='delete_user'),
    path('time_management/', TimeManagementView.as_view(), name='time_management'),
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('task_create/', TaskCreateView.as_view(), name='task_create'),
    path('task_delete/<int:pk>/', TaskDeleteView.as_view(), name='task_delete'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),  # Updated this line
    path('task_toggle_status/<int:pk>/', TaskToggleStatusView.as_view(), name='task_toggle_status'),
    path('list_create/', ListCreateView.as_view(), name='list_create'),
    path('list_edit/<int:pk>/', ListEditView.as_view(), name='list_edit'),
    path('list_list/', ListListView.as_view(), name='list_list'),
    path('add_task/', AddTaskView.as_view(), name='add_task'),
    path('delete_task/<int:pk>/', delete_task, name='delete_task'),
    path('list_toggle_status/<int:pk>/', ListToggleStatusView.as_view(), name='list_toggle_status'),
]
