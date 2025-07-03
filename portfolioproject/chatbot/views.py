from django.shortcuts import render

# Create your views here.
# chatbot/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatbotIntentResponse
from textblob import TextBlob

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").lower().strip()

        # Optional grammar correction
        try:
            corrected_input = str(TextBlob(user_input).correct())
        except:
            corrected_input = user_input

        # DB lookup
        entry = ChatbotIntentResponse.objects.filter(
            question__iexact=corrected_input
        ).first()

        if entry:
            response = entry.response
        else:
            response = "I'm sorry, I didn't understand that. ?"

        return JsonResponse({"response": response})

    return JsonResponse({"error": "Invalid request"}, status=400)
