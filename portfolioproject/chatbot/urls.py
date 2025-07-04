from django.urls import path

from chatbot import views

urlpatterns = [
    path('get_response/', views.chatbot_response, name='chatbot_response'),

]