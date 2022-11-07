from django.contrib import admin

from .models import Room, Message, Profile
from django.utils.text import slugify

from .models import Room, Message, Profile, Class

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug")







admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Profile)
admin.site.register(Class)
