from django.contrib import admin
from todo.models import TodoUser,TODO
# Register your models here.
class AdminTodoUser(admin.ModelAdmin):
    list_display = ['name','email','password']

admin.site.register(TodoUser,AdminTodoUser)
admin.site.register(TODO)