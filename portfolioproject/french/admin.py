from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from french.models import AboutMe,Experience,Skill,Qualification,Service

admin.site.register(AboutMe)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(Service)