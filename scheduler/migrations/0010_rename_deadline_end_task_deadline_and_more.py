# Generated by Django 4.1 on 2024-02-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0009_rename_usage_time_task_duration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='deadline_end',
            new_name='deadline',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='duration',
            new_name='usage_time',
        ),
        migrations.RemoveField(
            model_name='task',
            name='deadline_start',
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium', max_length=10),
        ),
    ]
