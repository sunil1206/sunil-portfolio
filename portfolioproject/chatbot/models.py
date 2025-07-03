# chatbot/models.py

from django.db import models

class ChatbotIntentResponse(models.Model):
    question = models.CharField(max_length=255, unique=True)
    response = models.TextField()

    def __str__(self):
        return self.question
