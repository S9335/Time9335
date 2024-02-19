# time_management/urls.py

from django.urls import path
from .views import (
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
    DeleteUserView,
    TaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskToggleStatusView,
    TaskUpdateView,
)

app_name = 'scheduler'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('delete_user/', DeleteUserView.as_view(), name='delete_user'),
    path('task_list/', TaskListView.as_view(), name='task_list'),
    path('add_task/', TaskCreateView.as_view(), name='add_task'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
    path('complete_task/<int:pk>/', TaskToggleStatusView.as_view(), name='complete_task'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
]
