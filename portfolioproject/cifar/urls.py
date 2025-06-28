from django.urls import path
from . import views

urlpatterns = [
    # path('', views.predict_image, name='predict_image'),
    path('predict/', views.predict_from_fastapi, name='predict_from_fastapi'),
    path('trash/', views.trash_predict_view, name='trash-predict'),
path('plant-disease/', views.plant_disease_predict_view, name='plant_disease_predict'),

# path('webcam/', views.webcam_predict, name='webcam_predict'),
]
