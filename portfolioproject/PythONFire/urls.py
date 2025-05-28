from django.urls import path

from PythONFire import views

urlpatterns = [
    path('', views.project_list_view, name='project-list'),
    path('swapcase/', views.swapcase_view, name='swapcase'),
    path('splitandjoin/', views.SplitandJoinstring, name='SplitandJoinstring'),
]