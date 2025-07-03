from django.urls import path

from portfolio import views
from portfolio.views import PortfolioDetailView

urlpatterns = [
    path('', views.index, name='index'),
path('portfolio/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),

]