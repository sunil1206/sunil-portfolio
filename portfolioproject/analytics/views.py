from django.shortcuts import render

# Create your views here.

# def analytics(request):
#     context = {
#     }
#     return render(request, 'dashboard/project_list.html', context)


# mlapp/views.py
from django.shortcuts import render, get_object_or_404
from .models import DataScienceProject, DashboardMetric


from django.shortcuts import render, get_object_or_404
from .models import DataScienceProject, EDA, MLModel
def project_list(request):
    """View to list all data science projects along with their related EDAs and ML models."""
    # Fetch all projects
    projects = DataScienceProject.objects.all()
    # Fetch all EDAs and ML models
    eda_list = EDA.objects.all()
    ml_models = MLModel.objects.all()
    # Pass the projects, EDA list, and ML model list to the context
    context = {
        'projects': projects,
        'eda_list': eda_list,
        'ml_models': ml_models,

    }
    return render(request, 'dashboard/project_list.html', context)

def eda_list(request):
    # Fetch all EDAs, projects, and ML models
    edas = EDA.objects.select_related('project').all()
    projects = DataScienceProject.objects.prefetch_related('eda').all()
    ml_models = MLModel.objects.all()

    # Pass the projects, EDA list, and ML model list to the context
    context = {
        'projects': projects,
        'eda_list': edas,
        'ml_models': ml_models,
    }
    return render(request, 'dashboard/eda_list.html', context)

def ml_model_list(request):
    # Fetch all EDAs, projects, and ML models
    edas = EDA.objects.select_related('project').all()
    projects = DataScienceProject.objects.all()
    ml_models = MLModel.objects.all()

    # Pass the projects, EDA list, and ML model list to the context
    context = {
        'projects': projects,
        'eda_list': edas,
        'ml_models': ml_models,
    }
    return render(request, 'dashboard/mlmodel_list.html', context)


def project_detail(request, slug):
    """View to display details of a specific data science project."""
    # Fetch the specific project based on the slug
    project = get_object_or_404(DataScienceProject, slug=slug)
    # Fetch related EDAs, ML models, and Dashboard metrics for this project
    eda_lists = EDA.objects.filter(project=project).order_by('-popularity') # Fetch EDAs for the specific project
    ml_models = MLModel.objects.filter(project=project)  # Fetch ML models for the specific project
    dashboard_metrics = DashboardMetric.objects.filter(project=project)  # Fetch metrics for the specific project
    projects = DataScienceProject.objects.all()
    # Fetch the specific EDA object
    # Fetch all EDAs and ML models
    eda_list = EDA.objects.all().order_by('-popularity')
    ml_model = MLModel.objects.all()
    context = {
        'project': project,  # The specific project
        'eda_list': eda_list,  # EDAs for this project
        'ml_models': ml_models,  # ML models for this project
        'dashboard_metrics': dashboard_metrics,  # Metrics for this project
        'projects':projects,
        'eda_lists':eda_lists,
        'ml_model':ml_model
    }
    return render(request, 'dashboard/project_detail.html', context)

def eda_detail(request, eda_id):
    """View to display details of a specific EDA analysis."""
    projects = DataScienceProject.objects.all()
    # Fetch the specific EDA object
    eda = get_object_or_404(EDA, id=eda_id)
    # Fetch all EDAs and ML models
    eda_list = EDA.objects.all()
    ml_models = MLModel.objects.all()

    # Fetch related data
    dashboard_metrics = DashboardMetric.objects.filter(project=eda.project)  # Metrics for the EDA's project
    eda_lists = EDA.objects.filter(project=eda.project).order_by('-popularity')  # EDAs related to the same project
    ml_model = MLModel.objects.filter(project=eda.project)  # ML models related to the same project

    # Prepare the context for rendering
    context = {
        'eda': eda,
        'eda_lists': eda_lists,
        'ml_model': ml_model,
        'dashboard_metrics': dashboard_metrics,
        'projects': projects,
        'eda_list': eda_list,
        'ml_models': ml_models,
    }

    return render(request, 'dashboard/eda_detail.html', context)


from django.shortcuts import get_object_or_404, render

def mlmodel_detail(request, model_id):
    projects = DataScienceProject.objects.all()
    # Fetch the specific EDA object
    # Fetch all EDAs and ML models
    eda_list = EDA.objects.all()
    ml_models = MLModel.objects.all()
    """View to display details of a specific ML model."""
    # Fetch the specific ML model
    ml_model = get_object_or_404(MLModel, id=model_id)

    # Fetch related data
    project = ml_model.project  # Get the associated project
    eda_lists = EDA.objects.filter(project=project)  # EDAs related to the same project
    related_ml_models = MLModel.objects.filter(project=project).exclude(id=model_id)  # Other ML models in the project
    dashboard_metrics = DashboardMetric.objects.filter(project=project)  # Metrics for the project

    # Prepare the context for rendering
    context = {
        'ml_model': ml_model,  # Specific ML model
        'project': project,  # Associated project
        'eda_list': eda_list,  # Related EDAs
        'related_ml_models': related_ml_models,  # Other ML models in the same project
        'dashboard_metrics': dashboard_metrics,  # Dashboard metrics
        'projects': projects,
        'eda_lists': eda_list,
        'ml_models': ml_models,
    }

    return render(request, 'dashboard/mlmodel_detail.html', context)

