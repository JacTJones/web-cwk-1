from rest_framework import serializers
from .models import Test, Story
from django.contrib.auth.models import User


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ["id", "name", "user"]


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "user"]


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = [
            "id",
            "headline",
            "category",
            "region",
            "details",
            "author",
            "story_date",
        ]
