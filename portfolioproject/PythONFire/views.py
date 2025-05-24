from django.shortcuts import render

from django.shortcuts import render

# Create your views here.
from PythONFire.models import PythonProject


def swapcase_view(request):
    projects = projects = PythonProject.objects.all().order_by('popularity')

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
