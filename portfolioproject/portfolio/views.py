from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from portfolio.models import AboutMe, Skill, Qualification, Experience, Portfolio, Service


def index(request):
    about_data = AboutMe.objects.first()
    skills = Skill.objects.all()
    education = Qualification.objects.order_by('order_number')
    experience = Experience.objects.order_by('order_number')
    portfolio_items = Portfolio.objects.order_by('-popularity')
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

    return render(request, 'index.html', context)





