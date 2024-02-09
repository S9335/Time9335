# scheduler/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    title = forms.CharField(label='タイトル')
    description = forms.CharField(label='説明', widget=forms.Textarea)
    priority = forms.ChoiceField(label='優先度', choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'onchange': 'changePriorityFont();'}))
    start_time = forms.DateTimeField(label='開始時間', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(label='終了時間', widget=forms.TextInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'start_time', 'end_time']
