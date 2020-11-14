from django.contrib import admin
from .models import Streamer, Videos, Comment
# Register your models here.

admin.site.register(Streamer)
# admin.site.register(Videos)


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ['streamer_name', 'vid_num', 'registered_dttm']
    list_filter = ['streamer_name']


@admin.register(Comment)
class CoomentAdmin(admin.ModelAdmin):
    list_filter = ['post']
