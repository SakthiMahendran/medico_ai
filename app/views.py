from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import ChatHistory
from .ai_handler import AIHandler  # Import the AIHandler class

# Reuse the shared instance of AIHandler
ai_handler = AIHandler()


def home(request):
    """
    Welcome page for the MedicoAI API.
    """
    return HttpResponse("<h1>Welcome to the MedicoAI API</h1><p>Use the appropriate API endpoints for interaction.</p>")


class PromptView(APIView):
    """
    Handles user prompts, generates chatbot responses using the shared AIHandler,
    and saves conversation history to the ChatHistory model.
    """

    def post(self, request, *args, **kwargs):
        # Extract prompt from request
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({"error": "Prompt is required"}, status=400)

        # Use the shared AIHandler to process the prompt
        response_text = ai_handler.process_prompt(prompt)
        conversation_history = ai_handler.get_conversation_history()

        # Save the conversation to the database
        chat = ChatHistory.objects.create(
            user=None,  # Replace with request.user if authentication is added
            chat_name="Default Chat",
            conversation=conversation_history
        )

        # Return the AI response and chat ID
        return Response({
            "response": response_text,
            "chat_id": chat.id,
            "conversation": conversation_history
        })


class ChatHistoryViewSet(ModelViewSet):
    """
    Provides CRUD operations for chat histories.
    """
    queryset = ChatHistory.objects.all()

    def get_queryset(self):
        """
        Optionally filter chat histories by the authenticated user.
        """
        return self.queryset


class UserLoginView(APIView):
    """
    Handles user login using session authentication.
    """
    def post(self, request, *args, **kwargs):
        return Response({"message": "Authentication is disabled for this view."})


class UserLogoutView(APIView):
    """
    Logs out the authenticated user.
    """
    def post(self, request, *args, **kwargs):
        return Response({"message": "Authentication is disabled for this view."})
