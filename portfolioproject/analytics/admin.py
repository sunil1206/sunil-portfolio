from django.contrib import admin

# Register your models here.
# mlapp/admin.py
from django.contrib import admin
from .models import DataScienceProject, EDA, MLModel,DashboardMetric

@admin.register(DataScienceProject)
class DataScienceProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'dataset_name', 'date_created', 'last_updated')
    search_fields = ('title', 'dataset_name')


@admin.register(EDA)
class EDAAdmin(admin.ModelAdmin):
    list_display = ('project','title','popularity', 'analysis_type','col_size')
    search_fields = ('project__title', 'analysis_type','col_size')


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('project', 'model_name')
    search_fields = ('project__title', 'model_name')
@admin.register(DashboardMetric)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ('project',)
    search_fields = ('project__title', )
