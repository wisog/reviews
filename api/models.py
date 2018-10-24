from . import utils
from django.db import models


class User(models.Model):
    auth_key = models.CharField(default=utils.generate_auth_key, max_length=20)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    def get_metadata(self):
        return "{name: {0}, email: {1}}".format(self.name, self.email)

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
Rating - must be between 1 - 5
Title - no more than 64 chars
Summary - no more than 10k chars
IP Address - IP of the review submitter
Submission date - the date the review was submitted
Company - information about the company for which the review was submitted, can be simple text (e.g., name, company id, etc.) or a separate model altogether
Reviewer Metadata - information about the reviewer, can be simple text (e.g., name, email, reviewer id, etc.) or a separate model altogether
"""

"""
Unit tests must be included providing 100% code coverage
Include instructions on local setup details for both “app setup” and “data setup”

Optional: 
Provide an authenticated admin view that allows me to view review submissions
Document the API

Organize the schema and data models in whatever manner you think makes the most sense and feel free to add any additional style and flair to the project that you'd like.
"""