from django.contrib import admin
from .models import ContactMe,Github

# Register your models here.
class AdminContactMe(admin.ModelAdmin):
    list_display = ['name','email','number','message']
class AdminGithub(admin.ModelAdmin):
    list_display = ['project_name','link','demolink']
admin.site.register(ContactMe,AdminContactMe)
admin.site.register(Github,AdminGithub)