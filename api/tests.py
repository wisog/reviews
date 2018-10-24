from django.test import TestCase
from api.models import User, Review


class UserTest(TestCase):

    @staticmethod
    def create_user(name, email):
        return User.objects.create(name=name, email=email)

    def test_create_user(self):
        user = self.create_user('cesar', 'cesar@algo.com')
        self.assertTrue(isinstance(user, User))
        print( User.objects.all())
