from django.urls import path
from .views import UserLoginView, UserLogoutView, UserCreateView

urlpatterns = [
    # User authentication endpoints
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    # User registration endpoint
    path('register/', UserCreateView.as_view(), name='user-register'),
]
