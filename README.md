BairesDev practice
@Author: wis0g

This is a test project, it contains an API to simulate a system of reviews generated by users.

Requirements:
Python 3.5+


INSTALL:
    pip install -r requirements

    There's no need for data creation, it's already loaded into db.sqlite3.
    If wants to clear everything, delete db.sqlite3 file and run:

    python manage.py migrate

    that will generate the DB file, 2 users:
        [{ 'username': 'cesar', 'password': 'qwerty'}, {'username': 'r2d2': 'password': 'qwerty'}]
    1 superuser:
        {'username': 'admin', 'password': 'admin'}

USE:

    python manage.py runserver

CONTENT:

    list of current users and a form for its creation:
    http://127.0.0.1:8000/api/v1/
    
    Authentication can be done using tokens with lifetime of 60 minutes, to obtain one check 
    /api/v1/token/ documentation at:
        http://127.0.0.1:8000/api/v1/docs/
    after that **EVERY REQUEST SHOULD BE SIGNED** using the obtained access token in the Headers, use:
    curl \
         -H "Authorization: Bearer long_string_obtained_as_access_field_on_token_call" \
        http://127.0.0.1:8000/api/v1/some-view/
    
    to get the list of reviews, send a GET request with Authorization header to:
        http://127.0.0.1:8000/api/v1/reviews/
    
    to retrieve one review, send a GET request with Authorization header to:
        http://127.0.0.1:8000/api/v1/reviews/{id}/
    
    to create a review, send a POST request with Authorization header to:
        http://127.0.0.1:8000/api/v1/reviews/
    the content_data should be a json with the format:
        {
            "rating": 1,
            "title": "title",
            "summary": "Summary for review",
            "company": "Company, any data to store"
        }

TEST:

    to test the app and get the code coverage report, run:    
    python manage.py test
    
    ![alt text](https://raw.githubusercontent.com/wisog/reviews/master/coverage_report.png)
