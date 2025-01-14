from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import chat_view, voice_input, voice_input_workflow

urlpatterns = [
    path('chat/', chat_view, name='therapy-session'),
    path('voice_input/', voice_input, name='voice_input'),  # URL for the HTML form
    path('voice_input_workflow/', voice_input_workflow, name='voice_input_workflow'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
