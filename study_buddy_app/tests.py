from django.contrib.auth.models import User
from django.test import TestCase
from .models import Profile
from django.dispatch import receiver 
from django.db.models.signals import post_save
from django.db import models
from .forms import UserForm
from .views import user
from study_buddy_app.models import Room, Message
from .models import Friends1
from .models import FriendRequest


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

class ChatTest(TestCase):
    def test_room_created(self):
        room = "this_is_a_test_room"
        new_room = Room.objects.create(name=room)
        new_room.save()
        self.assertIs(Room.objects.filter(name=room).exists(), True)
        
    def test_message_sent(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.last_name = 'Lennon'
        user.save()

        room = "this_is_a_test_room"
        new_room = Room.objects.create(name=room)
        new_room.save()

        new_message = Message.objects.create(value="hello world", user="john", room="this_is_a_test_room")
        new_message.save()
        self.assertIs(Message.objects.filter(value="hello world", user="john", room="this_is_a_test_room").exists(), True)


class FriendRequestTest(TestCase):
    def test_send_request(self):
        first_user = User.objects.create_user('me', 'me@example.com','mepassword')
        second_user = User.objects.create_user('you', 'you@example.com', 'youpassword')
        model = FriendRequest.objects.create(sender=first_user, receiver=second_user)
        self.assertIs(FriendRequest.objects.filter(sender=first_user,receiver=second_user).exists(), True)
    def test_friends(self):
        first_user = User.objects.create_user('me', 'me@example.com','mepassword')
        second_user = User.objects.create_user('you', 'you@example.com', 'youpassword')
        Friends1.make_friend(first_user, second_user)
        Friends1.make_friend(second_user, first_user)
        self.assertIs(Friends1.objects.filter(users1=first_user, current_user=second_user).exists(), True)
        self.assertIs(Friends1.objects.filter(users1=second_user, current_user=first_user).exists(), True)

class PublicProfileTests(TestCase):
    def test_public_profile(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, profile.slug)

    def test_public_profile_change_username(self):
        new_user = User.objects.create_user('Michael', 'Jackson@hehe.com', 'password123')
        new_user.username = 'CHANGEEEEEE'
        new_user.save()
        profile = Profile.objects.get(user=new_user)
        self.assertEqual(new_user.username, profile.slug)
        
        
