from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.dispatch import receiver #add this
from django.db.models.signals import post_save #add this
class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

# class Class(models.Model):
#     subject = models.CharField(max_length=4)
#     catalog_number = models.CharField(max_length=4)
#     course_section = models.CharField(max_length=3)

# class ClassList(models.Model):
#     class_list = models.ForeignKey(Class, on_delete=models.CASCADE)

class Profile(models.Model):  # add this class and the following fields

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # class_list = models.ForeignKey(ClassList, on_delete=models.CASCADE)
    @receiver(post_save, sender=User)  # add this
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)  # add this
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

