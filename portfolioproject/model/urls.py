from django.urls import path

from analytics import views

# urlpatterns = [
#     path('', views.analytics, name='analytics'),
#     path('projects/<slug:slug>/', project_detail, name='datascience_project_detail'),
#
# ]

from django.urls import path
from . import views


urlpatterns = [
path("predict_salary/", views.predict_salary, name="predict_salary"),
    path('predict_iris/', views.predict_iris, name='predict_iris'),
    path('predict_spotify/', views.predict_spotify, name='predict_spotify'),
]
