from django.urls import path
from . import views

urlpatterns = [
    # path('spam/', views.predict_spam, name='predict_spam'),
    path('predict-spam/', views.predict_spam, name='predict_spam'),
]
