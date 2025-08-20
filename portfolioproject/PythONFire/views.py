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


from django.shortcuts import render


# --- Custom Calculation Functions ---

def find_max(number_list):
    """
    Finds the maximum value in a list without using the built-in max().
    """
    # Start with the first element as the potential maximum
    max_value = number_list[0]
    # Loop through the rest of the list to find a larger number
    for number in number_list[1:]:
        if number > max_value:
            max_value = number
    return max_value


def find_min(number_list):
    """
    Finds the minimum value in a list without using the built-in min().
    """
    # Start with the first element as the potential minimum
    min_value = number_list[0]
    # Loop through the rest of the list to find a smaller number
    for number in number_list[1:]:
        if number < min_value:
            min_value = number
    return min_value


def bubble_sort(number_list):
    """
    Sorts a list in place using the bubble sort algorithm.
    """
    length = len(number_list)
    # Outer loop for the number of passes
    for i in range(length - 1):
        # Inner loop for comparisons and swaps
        for j in range(0, length - i - 1):
            if number_list[j] > number_list[j + 1]:
                # Swap elements if they are in the wrong order
                temp = number_list[j]
                number_list[j] = number_list[j + 1]
                number_list[j + 1] = temp
    return number_list


# --- Django View ---

def number_analyzer_view(request):
    projects = PythonProject.objects.all().order_by('popularity')
    """
    Handles the web request and performs number analysis using custom functions.
    """
    context = {'projects':projects}
    if request.method == 'POST':
        input_text = request.POST.get('input_numbers', '').strip()
        context['input_text'] = input_text

        if not input_text:
            context['error'] = "Input cannot be empty. Please enter some numbers."
            return render(request, 'python/analyzer.html', context)

        try:
            numbers = [int(num) for num in input_text.split()]
            if not numbers:
                raise ValueError("No valid numbers were provided.")

            # --- Calculations using custom functions ---
            min_value = find_min(numbers)
            max_value = find_max(numbers)

            # Create a copy of the list to sort, preserving the original
            numbers_to_sort = numbers.copy()
            sorted_numbers = bubble_sort(numbers_to_sort)

            # Add results to the context
            context['min_value'] = min_value
            context['max_value'] = max_value
            context['sorted_list'] = sorted_numbers
            context['original_list'] = numbers

        except ValueError:
            context['error'] = "Invalid input. Please enter only space-separated integers."

    return render(request, 'python/easy/analyzer.html', context)