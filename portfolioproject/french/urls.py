from django.urls import path

from french import views

urlpatterns = [
    path('', views.french, name='french'),

]