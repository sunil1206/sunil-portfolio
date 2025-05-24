from django.urls import path

from PythONFire import views
from PythONFire.views import swapcase_view

urlpatterns = [
    path('1/', views.swapcase_view, name='swapcase')
]