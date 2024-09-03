from rest_framework import serializers
from apps.parser.models import Log


class LogSerializer(serializers.ModelSerializer):
    """Сериализатор лога."""

    class Meta:
        model = Log
        fields = '__all__'
