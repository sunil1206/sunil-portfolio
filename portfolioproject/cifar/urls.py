from django.urls import path
from . import views

urlpatterns = [
    # path('', views.predict_image, name='predict_image'),
    path('predict/', views.predict_from_fastapi, name='predict_from_fastapi'),
# path('webcam/', views.webcam_predict, name='webcam_predict'),
]
