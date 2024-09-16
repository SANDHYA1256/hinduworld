# from django.shortcuts import render
# from rest_framework import viewsets, generics
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import organization, Country,continents
# from .serializers import OrgnisationSerializer, countrySerializer, continentsSerializer,OrgnisationSerializer1
# from .utils import save_image_to_folder
# from .pagination.org_pagination import OrganizationPagination
# from .pagination.orgbycountry_pagination import orgByCountryPagination
# from rest_framework.generics import ListAPIView


# class OrgnizationView(viewsets.ModelViewSet):
#     queryset = organization.objects.all()
#     serializer_class = OrgnisationSerializer
#     pagination_class = OrganizationPagination


# class AddOrgnization(generics.GenericAPIView):
#     serializer_class = OrgnisationSerializer1

#     def post(self, request, *args, **kwargs):
#         org_images = request.data.get('org_images')
#         print(org_images,"vfvfv")
#         request.data['org_images'] = "null"
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         if org_images and org_images != "null":
#             saved_location = save_image_to_folder(org_images, serializer.instance._id, serializer.instance.organization_name)
#             if saved_location:
#                 serializer.instance.org_images = saved_location
#                 print(serializer.instance.org_images,"referg")
#                 serializer.instance.save()
#                 return Response({
#                     "message": "success",
#                     "result": serializer.data
#                 })


# class GetItemByfield_InputView(generics.GenericAPIView):
#     serializer_class = OrgnisationSerializer
#     pagination_class = orgByCountryPagination

#     def get(self, request, input_value, field_name):
#         try:
#             field_names = [field.name for field in Country._meta.get_fields()]
#             if field_name in field_names:
#                 filter_kwargs = {field_name: input_value}
#                 queryset = organization.objects.filter(**filter_kwargs)
#                 serialized_data = OrgnisationSerializer(queryset, many=True)
#                 return Response(serialized_data.data)
#             else:
#                 return Response({
#                     'message': 'Invalid field name',
#                     'status': 400
#                 })
#         except organization.DoesNotExist:
#             return Response({
#                 'message': 'Object not found',
#                 'status': 404
#             })
        



# class CountryView(viewsets.ModelViewSet):
#     queryset = Country.objects.all()
#     serializer_class = countrySerializer

# class continentsView(viewsets.ModelViewSet):
#     queryset = continents.objects.all()
#     serializer_class = continentsSerializer





# class CountsView(APIView):
#     def get(self, request):
#         org_count = organization.objects.count()
#         country_count = Country.objects.count()
#         continent_count = continents.objects.values('continent').distinct().count()
        
#         return Response({
#             'organization_count': org_count,
#             'country_count':country_count,
#             'continent_count':continent_count
           
#         })



