from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'deadline', 'completed', 'user', 'usage_time', 'remaining_time')
    list_filter = ('completed', 'priority', 'deadline', 'user')
    search_fields = ('title', 'description')

    def remaining_time(self, obj):
        return obj.remaining_time

    remaining_time.short_description = 'Remaining Time'

