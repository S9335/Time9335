# scheduler/forms.py
from django import forms
from .models import Task
from django.utils import timezone

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

    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < timezone.now():
            raise forms.ValidationError('開始時間は現在時刻より後に設定してください。')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data.get('start_time')
        if start_time and end_time <= start_time:
            raise forms.ValidationError('終了時間は開始時間より後に設定してください。')
        return end_time

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'start_time', 'end_time']        
