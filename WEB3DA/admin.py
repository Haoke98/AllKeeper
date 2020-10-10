from django.contrib import admin

from .models import *


# Register your models here.
@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ['name', 'map']
