# Generated by Django 5.1 on 2024-09-03 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0004_todo_table_delete_todos'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo_table',
            name='todo_status',
            field=models.BooleanField(default=False),
        ),
    ]
