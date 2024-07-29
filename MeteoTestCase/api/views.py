from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import OnlyCitySerializer, CountrySerializer
from app.models import Country, City
from django.db.models import F


# Create your views here.
@api_view(['GET'])
def statistics(request):
	"""Для получения статистики по поиску"""
	if 'city' in request.GET:
		# По запросу города
		data = _get_city_stat(request.GET['city'])

	if 'country' in request.GET:
		# По запросу страны
		data = _get_country_stat(request.GET['country'])
	
	if not request.GET:
		data = _get_full_stat()

	return Response(data)


def _get_city_stat(name: str) -> Response:
	"""Для возвращения статистики по запросу города"""
	queryset = City.objects.filter(name=name).select_related().values('name', 'querys').annotate(country=F('country__name')).first()
	serializer = OnlyCitySerializer(queryset)
	return serializer.data


def _get_country_stat(name: str) -> Response:
	"""Для возвращения статистики по запросу страны"""
	country = Country.objects.filter(name=name).select_related().first()
	serializer = CountrySerializer(country)
	return serializer.data


def _get_full_stat():
	"""Для получения полной статистики"""
	queryset = Country.objects.all().select_related()
	serializer = CountrySerializer(queryset, many=True)
	return serializer.data
