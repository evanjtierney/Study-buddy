from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile
from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.db import models
from .forms import UserForm
from .views import user



class UserModelTests(TestCase):
    def test_user_created(self):
        #ejriejfoei
        """
        exists() returns True when a user was successfully created
        """
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.last_name = 'Lennon'
        user.save()
        self.assertIs(User.objects.filter(username='john').exists(), True)

class UserProfileTests(TestCase):
    def test_profile_created(self):
        new_user = User.objects.create_user('hello', 'what@hello.com', 'natpassword2')
        self.assertIs(Profile.objects.filter(user=new_user).exists(), True)
    def test_save_profile(self):
        new_user = User.objects.create_user('hello', 'what@hello.com', 'natpassword2')
        first_profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, 'hello')
        new_user.username = 'nat'
        new_user.save()
        second_profile = Profile.objects.get(user=new_user)
        self.assertEqual(first_profile, second_profile)
        self.assertEqual(new_user.username, 'nat')
