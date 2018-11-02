from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, viewsets, status

from .models import Review, User
from . import serializers


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Allows to get full list of reviews created by request's user, create new reviews
    or retrieve just one
    """
    permission_classes = (IsAuthenticated,)

    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def list(self, request, *args, **kwargs):
        all_reviews_for_user = self.queryset.filter(user=request.user)

        serializer = self.get_serializer(all_reviews_for_user, many=True)
        return Response(serializer.data)

    def retrieve(self, request, review_id=None):
        review = self.queryset.filter(user = request.user).filter(id = review_id).first()
        if review:
            serializer = self.get_serializer(review)
            return Response(serializer.data)
        return Response({
            'status': False,
            'message': 'not found or deleted'#'Review was not created.'
        }, status=status.HTTP_404_NOT_FOUND)


class UserListView(generics.ListCreateAPIView):
    """
    Allows to see the full list of users on the system and let create new ones
    """
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer