from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import ChatHistory, UploadedFile, User
from .ai_handler import AIHandler
from .serializers import ChatHistorySerializer, UploadedFileSerializer, UserSerializer

# Reuse the shared instance of AIHandler
ai_handler = AIHandler()


def home(request):
    """
    Welcome page for the MedicoAI API.
    """
    return HttpResponse("<h1>Welcome to the MedicoAI API</h1><p>Use the appropriate API endpoints for interaction.</p>")


class FileUploadView(APIView):
    """
    Handles file uploads.
    """
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided. Ensure you upload a file using 'file' key in form-data."}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = UploadedFile.objects.create(
            user=user,
            file_name=file.name,
            file_path=file
        )
        return Response({"message": "File uploaded successfully", "file_id": uploaded_file.id}, status=status.HTTP_201_CREATED)


class PromptView(APIView):
    """
    Handles user prompts and generates chatbot responses.
    """

    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        response_text = ai_handler.process_prompt(prompt)
        conversation_history = ai_handler.get_conversation_history()

        chat = ChatHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            chat_name="Default Chat",
            conversation=conversation_history
        )
        return Response({
            "response": response_text,
            "chat_id": chat.id,
            "conversation": conversation_history
        }, status=status.HTTP_200_OK)


class ChatHistoryViewSet(ModelViewSet):
    """
    Provides CRUD operations for chat histories.
    """
    queryset = ChatHistory.objects.all()
    serializer_class = ChatHistorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        """
        Handle creating new chat history.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user if request.user.is_authenticated else None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Handle updating existing chat history.
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deleting chat history.
        """
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Chat history deleted successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='list', url_name='chat-history-list')
    def chat_list(self, request, *args, **kwargs):
        """
        Custom action to list chat_id and chat_name as key-value pairs.
        """
        user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        chats = self.get_queryset()
        chat_list = [{"chat_id": str(chat.id), "chat_name": chat.chat_name} for chat in chats]
        return Response(chat_list, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    """
    Handles user login.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    """
    Logs out the authenticated user.
    """
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    """
    Handles user registration.
    """
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
