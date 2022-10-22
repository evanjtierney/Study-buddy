from django.contrib.auth.models import User
from django.test import TestCase
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
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.assertIs(Profile.create_user_profile(user, instance, created, **kwarges).exists(), True)
                     
    def test_save_profile(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.username='johnny'
        Profile.save_user_profile(user, instance, **kwargs)
        self.assertIs(Profile.objects.filter(username='johnny').exists(), True)
        
        

