from django.contrib.auth.models import User
from django.test import TestCase
class UserModelTests(TestCase):
    def test_user_created(self):
        """
        exists() returns True when a user was successfully created
        """
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.last_name = 'Lennon'
        user.save()
        self.assertIs(User.objects.filter(username='john').exists(), True)