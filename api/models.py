from . import utils
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(blank=False, default='test_user', max_length=50)

    def __str__(self):
        return self.name + ' ' + self.email


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    title = models.CharField(max_length=64)
    summary = models.TextField(max_length=10000)
    ip_address = models.CharField(max_length=15)
    submission_date = models.CharField(max_length=25, default=utils.get_today_as_string)
    company = models.CharField(max_length=60)

    def __str__(self):
        return self.title


"""
Unit tests must be included providing 100% code coverage
Include instructions on local setup details for both “app setup” and “data setup”

Optional: 
Provide an authenticated admin view that allows me to view review submissions
Document the API

Organize the schema and data models in whatever manner you think makes the most sense and feel free to add any additional style and flair to the project that you'd like.
"""