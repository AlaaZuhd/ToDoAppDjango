from django.contrib import admin
from .models import ToDoCategory, ToDoItem
# Register your models here.

admin.site.register(ToDoItem)
admin.site.register(ToDoCategory)
