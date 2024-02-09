# Generated by Django 4.1 on 2024-02-09 10:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0010_rename_deadline_end_task_deadline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('high', '高'), ('medium', '中'), ('low', '低')], default='medium', max_length=10),
        ),
    ]