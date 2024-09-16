from rest_framework import viewsets,generics
from ..models import Country,Organization,Continent
from ..serializers import countrySerializer,CountrySerializer1
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter






class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer1
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']  # Add the fields you want to search by

    # This is for cached data
    def list(self, request, *args, **kwargs):
        cache_key = 'countries_list'
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # Add field indicating data is from cache
            response_data = {'source': 'cache', 'data': cached_data}
            return Response(response_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=None)  # Cache indefinitely

        # Add field indicating data is from the database
        response_data = {'source': 'database', 'data': response.data}
        return Response(response_data)





class countries_by_Continent(generics.GenericAPIView):
    serializer_class = CountrySerializer1

    def get(self, request, continent):
        try:
            # Fetch the continent using the provided ID
            continent = Country.objects.filter(continent=continent)

            serialized_data=CountrySerializer1(continent,many=True)

            country_count = continent.count()

           
            return Response({
                "country_count": country_count,
                "countries": serialized_data.data
            }, status=status.HTTP_200_OK)
        
        except Continent.DoesNotExist:
            return Response({
                'message': 'Continent not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


