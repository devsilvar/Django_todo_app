# Generated by Django 5.1 on 2024-08-26 01:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='todo_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='todo',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
