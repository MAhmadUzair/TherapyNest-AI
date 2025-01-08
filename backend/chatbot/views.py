from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .utils.assistance import get_bot_response


@csrf_exempt
@require_GET
def chat_view(request):
    try:
        user_message = request.GET.get("user_message")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        bot_response = get_bot_response(user_message)

        return JsonResponse({
            "user_message": user_message,
            "bot_response": bot_response
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
