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
    path('project/', views.project_list, name='project_list'),  # List all projects
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),  # Project detail view
    path('eda/<int:eda_id>/', views.eda_detail, name='eda_detail'),  # EDA detail view
    path('mlmodel/<int:model_id>/', views.mlmodel_detail, name='mlmodel_detail'),  # MLModel detail view
path('eda-list/', views.eda_list, name='eda_list'),
    path('mlmodel-list/', views.ml_model_list, name='ml_model_list'),
]
