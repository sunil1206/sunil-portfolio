from django.urls import path
from . import views

urlpatterns = [
    # path('predict-spam/', views.predict_spam, name='predict_spam'),
    path('spam/', views.predict_spam, name='predict_spam'),
]
