# Generated by Django 4.1 on 2024-02-09 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0008_rename_deadline_task_deadline_end_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='usage_time',
            new_name='duration',
        ),
    ]
