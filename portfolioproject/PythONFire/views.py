from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from PythONFire.models import PythonProject
from analytics.models import DataScienceProject


def project_list_view(request):
    python_projects = PythonProject.objects.all()
    projects = DataScienceProject.objects.all()
    return render(request, 'python/python_list.html', {'projects': projects,'python_projects':python_projects})

def swapcase_view(request):
    projects = PythonProject.objects.all().order_by('popularity')
    result = ""
    if request.method == "POST":
        input_text = request.POST.get("input_text", "")
        # Manual swapcase logic
        for char in input_text:
            if char.islower():
                result += char.upper()
            elif char.isupper():
                result += char.lower()
            else:
                result += char  # Leave digits, punctuation, etc.
    return render(request, "python/1/swapcase.html", {"result": result,'projects':projects})

def SplitandJoinstring(request):
    projects = PythonProject.objects.all().order_by('popularity')
    output = ""
    input_string = ""
    if request.method == 'POST':
        input_string = request.POST.get("input_string", "")
        words = input_string.split(" ")
        output = '-'.join(words)
    return render(request, "python/easy/splitandjoin.html", {
        "input_string": input_string,
        "output": output,
        "projects": projects
    })

