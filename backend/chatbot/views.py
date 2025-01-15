from django.views.decorators.http import require_GET
from .utils.chat_assistant import get_bot_response
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.voice_assistant import handle_voice_input_audio


@csrf_exempt
@require_GET
def chat_view(request):
    user_message = request.GET.get("user_message")

    if not user_message:
        return JsonResponse({"error": "Message is required"}, status=400)

    try:
        bot_response = get_bot_response(user_message)
        return JsonResponse({"Assistant": bot_response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def voice_input_workflow(request):
    if request.method == "POST":
        audio_file = request.FILES.get('audio_data')

        if audio_file:
            try:
                audio_path = handle_voice_input_audio(audio_file)
                return JsonResponse({"audio_response_path": audio_path})
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            return JsonResponse({"error": "No audio data received"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def voice_input(request):
    return render(request, 'voice_input.html')
