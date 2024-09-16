from rest_framework import viewsets, generics
from ..models import Continent,organization,Country
from ..serializers.continent_serializer import continentsSerializer
from ..serializers.country_serializer import countrySerializer
from rest_framework.response import Response
from rest_framework import status


class continentsView(viewsets.ModelViewSet):
    queryset = Continent.objects.all()
    serializer_class = continentsSerializer







