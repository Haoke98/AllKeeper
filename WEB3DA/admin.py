from django.contrib import admin

from miniProgram.admin import MyModelAdmin
from .models import *


# Register your models here.
@admin.register(Map)
class MapAdmin(MyModelAdmin):
    list_display = MyModelAdmin.list_display + ['_map']

    def _map(self, obj):
        return obj.map
