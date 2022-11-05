from django.contrib import admin

from .models import Room, Message, Profile, Class
from django.utils.text import slugify

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug")







admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Class)