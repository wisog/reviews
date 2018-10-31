from django.test import TestCase, Client
from api.models import User, Review
import json

class ModelsTest(TestCase):

    @staticmethod
    def create_user(username,email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.name = 'testing'
        return user

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
        user = self.create_user('user1', 'cesar@algo.com', 'test')
        self.assertTrue(isinstance(user, User))
        self.assertEquals(str(user), 'testing cesar@algo.com')

    def test_create_review(self):
        user = self.create_user('user2', 'pepe@algo.com', 'test')
        review = self.create_review(user)
        self.assertTrue(isinstance(review, Review))
        self.assertEqual(str(review.title), 'title')
        self.assertEqual(review.user, user)

    def test_create_review_bad_parameters(self):
        user = self.create_user('user2', 'pepe@algo.com', 'test')
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 401)

    def test_get_user_token(self):
        token = self.client.post('/api/v1/token/', {"username": 'cesar', "password": 'qwerty'})
        self.assertEqual(token.status_code, 200)
        token_data = json.loads(token.content.decode("utf-8") )
        self.assertTrue('access' in token_data)

    def test_get_users_list(self):
        users = self.client.get('/api/v1/')
        users_data = json.loads(users.content.decode("utf-8"))
        self.assertTrue(len(users_data)>0)

    def test_get_review(self):
        token = self.client.post('/api/v1/token/', {"username": 'cesar', "password": 'qwerty'})
        token_data = json.loads(token.content.decode("utf-8"))
        access_token = token_data['access']
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        review = self.client.get('/api/v1/reviews/1/')
        self.assertTrue(review.status_code != 401)

