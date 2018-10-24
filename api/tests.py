from django.test import TestCase
from api.models import User, Review


class UserTest(TestCase):

    @staticmethod
    def create_user(name, email):
        return User.objects.create(name=name, email=email)

    @staticmethod
    def create_review(user, rating = 'rating', title='title', summary='summary',
                      ip_address = 'ip_address', company='company'):
        review = Review()
        review.user = user
        review.rating = rating
        review.title = title
        review.summary = summary
        review.ip_address = ip_address
        review.company = company
        return review

    def test_create_user(self):
        user = self.create_user('cesar', 'cesar@algo.com')
        self.assertTrue(isinstance(user, User))
        #print( User.objects.all())

    def test_create_review(self):
        user = self.create_user('Pepe', 'pepe@algo.com')
        review = self.create_review(user)
        self.assertTrue(isinstance(review, Review))
        self.assertTrue(review.company == 'company')

