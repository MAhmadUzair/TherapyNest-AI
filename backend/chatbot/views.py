from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .utils.assistant import get_bot_response


@csrf_exempt
@require_GET
def chat_view(request):
    user_message = request.GET.get("user_message")

    if not user_message:
        return JsonResponse({"error": "Message is required"}, status=400)

    try:
        bot_response = get_bot_response(user_message)
        # print (f'response {bot_response}')
        return JsonResponse({"Assistant": bot_response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

