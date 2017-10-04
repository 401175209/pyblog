from django.contrib import admin

# Register your models here.
from .models import comment

class commentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'text', 'post', 'time']

admin.site.register(comment,commentsAdmin)