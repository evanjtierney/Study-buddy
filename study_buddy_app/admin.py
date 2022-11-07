from django.contrib import admin



from .models import Room, Message, Profile, Class

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "slug")

class ClassAdmin(admin.ModelAdmin):
    list_display = ("subject", "catalog_number", "course_section")





admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Class, ClassAdmin)
