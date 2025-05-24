from django.contrib import admin

# Register your models here.
from portfolio.models import AboutMe,Experience,Skill,Qualification,Portfolio,Service
class PortfolioAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ('name', 'category')
admin.site.register(AboutMe)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(Portfolio,PortfolioAdmin)
admin.site.register(Service)
