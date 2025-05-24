from django.shortcuts import render

# Create your views here.
from french.models import AboutMe, Skill, Qualification, Experience, Service
from portfolio.models import Portfolio


def french(request):
    about_data = AboutMe.objects.first()
    skills = Skill.objects.all()
    education = Qualification.objects.order_by('order_number')
    experience = Experience.objects.order_by('order_number')
    portfolio_items = Portfolio.objects.all()
    category_choices = Portfolio.CATEGORY_CHOICES
    services = Service.objects.all()

    context = {
        'about_data': about_data,
        'education': education,
        'experience': experience,
        'skills': skills,
        'portfolio_items': portfolio_items,
        'category_choices': category_choices,
        'services':services,
    }

    return render(request, 'french.html', context)