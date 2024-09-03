from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription
from api.v1.serializers.course_serializer import CourseSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""
    user = CustomUserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Subscription
        fields = '__all__'
