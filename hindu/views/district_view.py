from rest_framework import viewsets
from ..models import District,State
from ..serializers import DistrictSerializer
from rest_framework .response import Response
from rest_framework import generics,status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



class DistrictVIew(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'state']  # Add the fields you want to search by

    def list(self, request):
        filter_kwargs = {}

        for key, value in request.query_params.items():
            filter_kwargs[key] = value

        try:
            queryset = District.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                })

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serialized_data = DistrictSerializer(queryset, many=True)
            return Response(serialized_data.data)

        except District.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            })







class districts_By_State(generics.GenericAPIView):
    serializer_class = DistrictSerializer

    def get(self, request, state):
        try:
            # Fetch the districts using the provided state
            districts = District.objects.filter(state=state)

            serialized_data = DistrictSerializer(districts, many=True)
            district_count = districts.count()

            return Response({
                "district_count": district_count,
                "districts": serialized_data.data
            }, status=status.HTTP_200_OK)
        
        except State.DoesNotExist:
            return Response({
                'message': 'State not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                'message': str(e),
                'status': 500
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)