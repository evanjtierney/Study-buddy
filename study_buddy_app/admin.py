from django.contrib import admin
from .models import Room, Message, Profile, Class

# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Class)