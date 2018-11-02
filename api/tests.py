from django.test import TestCase, Client
from api.models import User, Review
import json


class ModelsTest(TestCase):

    token = None

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

    def add_headers_auth(self):
        if self.token is None:
            token = self.client.post('/api/v1/token/', {"username": 'cesar', "password": 'qwerty'})
            token_data = json.loads(token.content.decode("utf-8"))
            self.token = token_data['access']

        self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + self.token

    def test_create_user(self):
        user = self.create_user('user1', 'cesar@algo.com', 'test')
        self.assertTrue(isinstance(user, User), "Instance not created")
        self.assertEquals(str(user), 'testing cesar@algo.com', "It's not invoking custom model __str__")

    def test_create_review(self):
        user = self.create_user('user2', 'pepe@algo.com', 'test')
        review = self.create_review(user)
        self.assertTrue(isinstance(review, Review), "Instance not created")
        self.assertEqual(str(review.title), 'title', "Instance created wrong")
        self.assertEqual(review.user, user, "The user for that review have wrong or null association")

    def test_get_review_no_access(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 401, "It should return 401 for this view")

    def test_get_reviews(self):
        self.add_headers_auth()
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200, "Should receive list of reviews no matter if it's empty list")

    def test_get_user_token(self):
        token = self.client.post('/api/v1/token/', {"username": 'cesar', "password": 'qwerty'})
        self.assertEqual(token.status_code, 200, "Received error on token creation")
        token_data = json.loads(token.content.decode("utf-8"))
        self.assertTrue('access' in token_data, "it didn't receive correct access token")

    def test_get_users_list(self):
        users = self.client.get('/api/v1/')
        users_data = json.loads(users.content.decode("utf-8"))
        self.assertTrue(len(users_data)>0, "Users table are empty")

    def test_get_review(self):
        self.add_headers_auth()
        review = self.client.get('/api/v1/reviews/1/')
        self.assertTrue(review.status_code != 401, "It should've returned 401 HTTP Error")

    def test_create_review_bad_params(self):
        self.add_headers_auth()
        review = {
            'rating': 0,
            'title': 'review',
            'summary': 'That was a really great item',
            'company': 'Sarape labs'
        }

        response = self.client.post('/api/v1/reviews/', review)
        error = json.loads(response.content.decode("utf-8"))
        self.assertTrue("non_field_errors" in error, "Error message not showing")
        self.assertEqual(["rating should be between 1 and 5"], error["non_field_errors"], "Incorrect error message")

    def test_create_review(self):
        self.add_headers_auth()
        review = {
            'rating': 5,
            'title': 'review',
            'summary': 'That was a really great item',
            'company': 'Sarape labs'
        }

        response = self.client.post('/api/v1/reviews/', review)
        self.assertEquals(response.status_code, 201)
        json_data = json.loads(response.content.decode("utf-8"))
        id_review = json_data["id"]
        # Retrieve the created review
        review = self.client.get('/api/v1/reviews/'+str(id_review)+'/')
        json_data2 = json.loads(review.content.decode("utf-8"))
        self.assertEquals(id_review, json_data2["id"], "It received wrong data")
