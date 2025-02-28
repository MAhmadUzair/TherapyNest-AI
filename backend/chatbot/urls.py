from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import voice_input, voice_input_workflow, FinancialAssistantAPI

urlpatterns = [
    path('financial-assistant/', FinancialAssistantAPI.as_view(), name='financial-assistant'),
    path('voice_input/', voice_input, name='voice_input'),  # URL for the HTML form
    path('voice_input_workflow/', voice_input_workflow, name='voice_input_workflow'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
