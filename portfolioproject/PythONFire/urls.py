from django.urls import path

from PythONFire import views

urlpatterns = [
    path('swapcase/', views.swapcase_view, name='swapcase'),
    path('', views.project_list_view, name='project-list'),
]