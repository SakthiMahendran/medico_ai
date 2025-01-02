"""
URL configuration for medico_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app.views import home  
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    path('user/', include('app.auth_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
Your are django backend developer now you have design a API schema for a django backend for my junior developers to understand based on the applicastion 
discritopiong...
<Discription>
The applicatoin is a Health Care chatbot applicatoin that uses langchain that the feauture are 
There will be a file upload button, the user may able to upload the file using a file upload button,
the use may type and send the prompt, the chatbot will respond to it, there will be chathistroy that 
holds all the previous converstation, with required metadata 
<Discrpiton>

Design an API schema and Modle schema with sample code with proper explaination for my junior developer to 
implement it
"""