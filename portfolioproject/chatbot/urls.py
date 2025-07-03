from django.urls import path

from PythONFire import views

urlpatterns = [
path("chatbot/", views.chatbot_response, name="chatbot-response"),

]