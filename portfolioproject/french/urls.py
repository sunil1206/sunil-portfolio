from django.urls import path

from french import views
from portfolio import views
urlpatterns = [
    path('', views.index, name='index'),

]