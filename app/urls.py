from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PromptView,
    ChatHistoryViewSet,
    FileUploadView,
    UserLoginView,
    UserLogoutView,
    UserCreateView
)

# Initialize a router for ChatHistoryViewSet
router = DefaultRouter()
router.register(r'chat-history', ChatHistoryViewSet, basename='chat-history')

# App-specific URL patterns
urlpatterns = [
    # File upload endpoint
    path('upload/', FileUploadView.as_view(), name='file-upload'),

    # Chat prompt endpoint
    path('prompt/', PromptView.as_view(), name='prompt'),

    # Explicit routes for chat history CRUD
    path('chat-history/create/', ChatHistoryViewSet.as_view({'post': 'create'}), name='chat-history-create'),
    path('chat-history/update/<str:pk>/', ChatHistoryViewSet.as_view({'put': 'update'}), name='chat-history-update'),
    path('chat-history/delete/<str:pk>/', ChatHistoryViewSet.as_view({'delete': 'destroy'}), name='chat-history-delete'),

    # Custom endpoint to list chat IDs and names
    path('chat-history/list/', ChatHistoryViewSet.as_view({'get': 'chat_list'}), name='chat-history-list'),

    # Include router-generated endpoints for ChatHistoryViewSet
    path('', include(router.urls)),
]
