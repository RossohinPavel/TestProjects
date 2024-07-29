from rest_framework import serializers
from app.models import City


class OnlyCitySerializer(serializers.Serializer):
	"""Сериализатор для модели городов"""
	name = serializers.CharField()
	querys = serializers.IntegerField()
	country = serializers.CharField()


class CitySerializer(serializers.ModelSerializer):

	class Meta:
		model = City
		exclude = ('id', "country")


class CountrySerializer(serializers.Serializer):
	"""Сериализатор для модели стран"""
	name = serializers.CharField()
	querys = serializers.IntegerField()
	citys = CitySerializer(many=True)
