from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from analytics.models import DataScienceProject
from portfolio.models import AboutMe, Skill, Qualification, Experience, Portfolio, Service, Tools


def index(request):
    about_data = AboutMe.objects.first()
    skills = Skill.objects.all()
    education = Qualification.objects.order_by('order_number')
    experience = Experience.objects.order_by('order_number')
    portfolio_items = Portfolio.objects.order_by('-popularity')
    category_choices = Portfolio.CATEGORY_CHOICES
    services = Service.objects.all()
    datascience_projects = DataScienceProject.objects.order_by('-popularity')
    tools = Tools.objects.order_by('-popularity')


    # Group tools by category
    tools_by_category = {
        "Programming Languages": tools.filter(category='programming'),
        "DevOps": tools.filter(category='devops'),
        "Visualization": tools.filter(category='visualization'),
        "Databases": tools.filter(category='database'),
    }

    context = {
        'about_data': about_data,
        'education': education,
        'experience': experience,
        'skills': skills,
        'portfolio_items': portfolio_items,
        'category_choices': category_choices,
        'services':services,
        'datascience_projects':datascience_projects,
        'tools_by_category':tools_by_category,
        'tools':tools,
    }

    return render(request, 'index.html', context)

from django.views.generic import DetailView
class PortfolioDetailView(DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio_detail.html'
    context_object_name = 'portfolio'



