"""time_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from scheduler.views import CustomLoginView, CustomLogoutView, TimeManagementView, TaskCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scheduler/login/', CustomLoginView.as_view(), name='login'),
    path('scheduler/logout/', CustomLogoutView.as_view(), name='logout'),
    path('scheduler/time_management/', TimeManagementView.as_view(), name='time_management'),
    path('scheduler/add_task/', TaskCreateView.as_view(), name='add_task'),
    path('scheduler/', include('scheduler.urls', namespace='scheduler')),
    path('', TimeManagementView.as_view(), name='home'), 
]
