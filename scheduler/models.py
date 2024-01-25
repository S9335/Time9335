# scheduler/models.py
from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    usage_time = models.DurationField(default=timezone.timedelta(0))

    def __str__(self):
        return self.title

    def remaining_time(self):
        if self.deadline > timezone.now():
            return self.deadline - timezone.now()
        return timezone.timedelta(0)

