from django.contrib import admin

from .models import kino, episode


# Register your models here.
@admin.register(kino)
class kinoAdmin(admin.ModelAdmin):
    list_display = ['name', 'cover', ]


@admin.register(episode)
class episodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'content', 'kino']
