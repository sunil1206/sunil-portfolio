from django.contrib import admin

# Register your models here.
from .models import PythonProject

@admin.register(PythonProject)
class PythonProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'popularity', 'created_date', 'url')
    search_fields = ('name',)
    list_filter = ('created_date',)