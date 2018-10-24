from django.http import HttpResponse

from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotFound

from django.forms.models import model_to_dict

import json

from .utils import get_user_from_key, MESSAGES
from .models import Review


def review(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        if 'authkey' not in data:
            return HttpResponseForbidden(json.dumps({'message': MESSAGES['NO_KEY']}))
        user = get_user_from_key(data['authkey'])
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': "user don't exist for that key"}))
        if 'rating' not in data or 'title' not in data or 'summary' not in data or 'company' not in data:
            return HttpResponseBadRequest("{'message': 'missing fields'}")

        rating = data["rating"]
        title = data["title"]
        summary = data["summary"]
        ip_address = request.META.get('REMOTE_ADDR')
        company = data["company"]
        # object Review construction
        new_review = Review()
        new_review.user = user
        new_review.rating = rating
        new_review.title = title
        new_review.summary = summary
        new_review.ip_address = ip_address
        new_review.company = company
        new_review.save()
        #data = serializers.serialize("json", [new_review])

        return HttpResponse(json.dumps(model_to_dict(new_review)), content_type="application/json")
        #return JsonResponse(data, safe=False)
    elif request.method == "GET":
        auth_key = request.GET.get('authkey', None)
        if auth_key is None:
            return HttpResponseForbidden(json.dumps({'message': 'should provide a valid authkey param'}))
        user = get_user_from_key(auth_key)
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': "user don't exist for that key"}))

        results = Review.objects.all().filter(user=user)
        data = [ model_to_dict(result) for result in results]

        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponseForbidden("Method not supported")


def one_review(request, review_id):
    if request.method == "GET":
        auth_key = request.GET.get('authkey', None)
        if auth_key is None:
            return HttpResponseForbidden(json.dumps({'message': 'should provide a valid authkey param'}))
        user = get_user_from_key(auth_key)
        if user is None:
            return HttpResponseForbidden(json.dumps({'message': "user don't exist for that key"}))

        result = Review.objects.all().filter(user=user).filter(id=review_id).first()
        if result is None:
            return HttpResponseNotFound(json.dumps({'message': "review doesn't exist or deleted"}))
        data = model_to_dict(result)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponseForbidden(json.dumps({'message': MESSAGES['BAD_METHOD']}))
