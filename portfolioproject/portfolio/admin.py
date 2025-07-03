from django.contrib import admin

# Register your models here.
from portfolio.models import AboutMe, Experience, Skill, Qualification, Portfolio, Service


class PortfolioAdmin(admin.ModelAdmin):
    # Specify the fields you want to display in the list view
    list_display = ('name', 'category')
admin.site.register(AboutMe)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Skill)
admin.site.register(Portfolio,PortfolioAdmin)
admin.site.register(Service)


from .models import Tools

class ToolsAdmin(admin.ModelAdmin):
    # Customize the fields that will appear in the list view
    list_display = ('name', 'category', 'percentage', 'progress_bar_color', 'image_tag')

    # Add search functionality
    search_fields = ('name',)

    # Add filters for easier management of categories
    list_filter = ('category', 'progress_bar_color')

    # If you want the image to be clickable and show a thumbnail in the list view:
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
        return "No image"

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

# Register the model and the custom admin class
admin.site.register(Tools, ToolsAdmin)