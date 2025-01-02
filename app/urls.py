from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromptView, ChatHistoryViewSet

router = DefaultRouter()
router.register(r'chat-history', ChatHistoryViewSet, basename='chat-history')

urlpatterns = [
    #path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('prompt/', PromptView.as_view(), name='prompt'),
    path('', include(router.urls)),
]
