# scheduler/forms.py
from django import forms
from .models import Task, List

class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]

    title = forms.CharField(label='タイトル')
    description = forms.CharField(label='説明', widget=forms.Textarea)
    priority = forms.ChoiceField(label='優先度', choices=PRIORITY_CHOICES)
    usage_time = forms.DurationField(label='利用時間')

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'usage_time']

class ListForm(forms.ModelForm):
    title = forms.CharField(label='タイトル') 

    class Meta:
        model = List
        fields = ['title'] 
