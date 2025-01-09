from django.urls import path
from . import views
from .views import chat_view

urlpatterns = [
    path('chat/', chat_view, name='therapy-session'),
]
