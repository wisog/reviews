from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound
from django.forms.models import model_to_dict

import json

from .utils import get_user_from_key, MESSAGES, generate_review_from_data
from .models import Review


def review(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if 'authkey' not in data:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['NO_KEY']}))
        user = get_user_from_key(data['authkey'])
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_KEY']}))
        if 'rating' not in data or 'title' not in data or 'summary' not in data or 'company' not in data:
            return HttpResponseBadRequest(json.dumps({'message': MESSAGES['BAD_FIELDS']}))

        new_review = generate_review_from_data(data, request, user)

        return HttpResponse(json.dumps(model_to_dict(new_review)), content_type="application/json")
    elif request.method == "GET":
        auth_key = request.GET.get('authkey', None)
        if auth_key is None:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['NO_KEY']}))
        user = get_user_from_key(auth_key)
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_KEY']}))

        results = Review.objects.all().filter(user=user)
        data = [ model_to_dict(result) for result in results]

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_METHOD']} ))


def one_review(request, review_id):
    if request.method == "GET":
        auth_key = request.GET.get('authkey', None)
        if auth_key is None:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['NO_KEY'] }))
        user = get_user_from_key(auth_key)
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_KEY'] }))

        result = Review.objects.all().filter(user=user).filter(id=review_id).first()
        if result is None:
            return HttpResponseNotFound(json.dumps({'message': MESSAGES['REVIEW_NOT_FOUND']}))
        data = model_to_dict(result)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_METHOD']}))
