# Generated by Django 5.1.2 on 2025-01-01 10:16

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedfile',
            name='user',
        ),
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('chat_name', models.CharField(max_length=255)),
                ('conversation', models.JSONField(default=dict)),
                ('file_embeddings', models.BinaryField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='app.user')),
            ],
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='UploadedFile',
        ),
    ]
