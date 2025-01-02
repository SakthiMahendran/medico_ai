from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Avoid clash with default reverse accessor
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",  # Avoid clash with default reverse accessor
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username


class ChatHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats", null=True, blank=True)  # Optional user
    chat_name = models.CharField(max_length=255, default="New Chat")  # Default chat name
    conversation = models.JSONField(default=dict)  # Conversation as JSON
    file_embeddings = models.BinaryField(null=True, blank=True)  # Optional binary embeddings
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Update timestamp

    def __str__(self):
        return f"Chat {self.chat_name} by {self.user.username if self.user else 'Anonymous'}"








'''from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Avoid clash with default reverse accessor
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",  # Avoid clash with default reverse accessor
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    response = models.TextField()
    file = models.ForeignKey(UploadedFile, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)'''

# Create your models here.
