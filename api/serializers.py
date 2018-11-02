from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('name', 'email', 'username', )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=64)
    company = serializers.CharField()
    rating = serializers.IntegerField()
    summary = serializers.CharField(max_length=10000)

    def to_internal_value(self, data):
        request = self.context['request']
        data['ip_address'] = request.META.get('REMOTE_ADDR')
        data['user'] = self.context['request'].user
        return data

    def validate(self, data):
        """
        custom check based on logic for this model
        """
        if data['rating'] < 1 or data['rating'] > 5:
            raise serializers.ValidationError("rating should be between 1 and 5")

        return data

    class Meta:
        model = models.Review
        fields = ('id', 'user','title','company','rating','summary','ip_address','submission_date',)
