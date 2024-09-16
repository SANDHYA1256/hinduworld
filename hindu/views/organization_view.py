from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Organization, Country,Continent,Register,District
from ..serializers.organization_serializer import OrgnisationSerializer,OrgnisationSerializer1,OrgnisationSerializer2,OrganizationSerializer4
from ..utils import save_image_to_folder
from ..pagination.org_pagination import OrganizationPagination
from ..pagination.orgbycountry_pagination import orgByCountryPagination
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import FieldDoesNotExist


from rest_framework import viewsets, pagination

class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000 








####################  AddOrgnization as per single register and login ########################
class AddOrgnization(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Fetch the Register instance for the logged-in user using some identifier
            username = request.user.username  # Example: Using username
            print(f"Username: {username}")
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member
            print(f"is_member: {is_member}")

            # Check if the user is a member
            if is_member == "FALSE":
                print("User is not a member")
                return Response({
                    "message": "Cannot create organization. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Capture the current time
            created_at = datetime.now()

            # Proceed with organization creation
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # Handle organization images and logo if provided
            org_images = request.data.get('org_images')
            org_logo = request.data.get('org_logo')
            govt_id_proof=request.data.get('govt_id_proof')

            if org_images and org_images != "null":
                saved_location = save_image_to_folder(org_images, serializer.instance._id, serializer.instance.organization_name,'hinduworldimages')
                if saved_location:
                    serializer.instance.org_images = saved_location

            if org_logo and org_logo != "null":
                # saved_logo_location = save_logo_to_folder(org_logo, serializer.instance._id, serializer.instance.organization_name)
                saved_logo_location = save_image_to_folder(org_logo, serializer.instance._id, serializer.instance.organization_name,'hinduworldlogos')
                if saved_logo_location:
                    serializer.instance.org_logo = saved_logo_location




            if govt_id_proof and govt_id_proof != "null":
                saved_govt_id_proof_location = save_image_to_folder(govt_id_proof, serializer.instance._id, serializer.instance.organization_name,'orgdocument')
                if saved_govt_id_proof_location:
                     serializer.instance.govt_id_proof = saved_govt_id_proof_location

            serializer.instance.save()

            # Send email to EMAIL_HOST_USER
            send_mail(
                'New Organization added',
                f'User ID: {request.user.id}\n'
                f'Contact Number: {register_instance.contact_number}\n'
                f'full Name: {request.user.full_name}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Organization ID: {serializer.instance._id}\n'
                f'Organization Name: {serializer.instance.organization_name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "Organization added successfully.",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Register.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















class GetItemByfield_InputView(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer
    pagination_class = orgByCountryPagination

    def get(self, request, input_value, field_name):
        try:
            field_names = [field.name for field in Organization._meta.get_fields()]
            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Organization.objects.filter(**filter_kwargs)
                serialized_data = OrgnisationSerializer(queryset, many=True)
                return Response(serialized_data.data)
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })
        except Organization.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })
        






class GetItemByfields_InputViews(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer
    pagination_class = orgByCountryPagination

    def get(self, request, input_value1, field_name1, input_value2=None, field_name2=None):
        try:
            field_names = [field.name for field in Organization._meta.get_fields()]
            filter_kwargs = {}


            if field_name1 in field_names:
                filter_kwargs[field_name1] = input_value1

                
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': 400
                })
            if field_name2 and input_value2:
                if field_name2 in field_names:
                    filter_kwargs[field_name2] = input_value2

                else:
                    return Response({
                        'message': f'Invalid field name: {field_name2}',
                        'status': 400
                    })
                
            queryset = Organization.objects.filter(**filter_kwargs)
            serialized_data = OrgnisationSerializer(queryset, many=True)
            return Response(serialized_data.data)
            
        except Organization.DoesNotExist:
            return Response({
                'message': 'Object not found',
                'status': 404
            })
        











class GetOrgByStatus_Pending(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1

    def get(self, request):
        orgs = Organization.objects.filter(status='PENDING')  # Filter by 'PENDING' status
        
        if not orgs.exists():
            return Response({
                'message': 'No organizations found with PENDING status',
                'result': []
            })

        serializer = self.get_serializer(orgs, many=True)
        return Response({
            'message': 'success',
            'result': serializer.data
        })
        
class GetOrgByStatus_Success(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer1

    def get(self, request):
        orgs = Organization.objects.filter(status='SUCCESS')  # Filter by 'PENDING' status
        
        if not orgs.exists():
            return Response({
                'message': 'No organizations found with SUCCESS status',
                'result': []
            })

        serializer = self.get_serializer(orgs, many=True)
        return Response({
            'message': 'success',
            'result': serializer.data
        }) 




class UpdateOrgStatus(generics.GenericAPIView):
    serializer_class = OrgnisationSerializer2

    def put(self, request, org_id):
        try:
            org = Organization.objects.get(pk=org_id, status='PENDING')
        except Organization.DoesNotExist:
            return Response({
                'message': 'Organization with PENDING status not found for the provided ID'
            }, status=http_status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        org.status = 'SUCCESS'
        org.save()

        # Serialize the updated organization
        serializer = self.get_serializer(org)

        return Response({
            'message': 'success',
            'result': serializer.data
        })












class GetbyCountryLocationorganization(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        country_id = self.kwargs.get('country_id')
        organization_in_country = Organization.objects.filter(
            object_id__block__district__state__country_id=country_id
        )
        return organization_in_country


  








class GetItemBystatefield_location(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        state_id = self.kwargs.get('state_id')
        organizations_in_state = Organization.objects.filter(object_id__block__district__state_id=state_id)
        return organizations_in_state
    


class GetbyDistrictLocationOrganization(generics.ListAPIView):
    serializer_class = OrgnisationSerializer

    def get_queryset(self):
        district_id =self.kwargs.get('district_id')
        organizations_in_district = Organization.objects.filter(object_id=district_id)
        return organizations_in_district
    





class OrgnizationView(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer4
    pagination_class = OrganizationPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        'organization_name', 
        'object_id__state__name', 
        'object_id__state__country__name', 
        'object_id__state__country__continent__name'
    ]



    @action(detail=False, methods=['get'], url_path='by-field/(?P<field_name>[^/.]+)/(?P<input_value>[^/.]+)')
    def get_item_by_field(self, request, field_name=None, input_value=None):
        if not input_value or not field_name:
            return Response({
                'message': 'Field name and input value are required',
                'status': status.HTTP_400_BAD_REQUEST
            })

        try:
            field_names = [field.name for field in Organization._meta.get_fields()]
            if field_name in field_names:
                filter_kwargs = {field_name: input_value}
                queryset = Organization.objects.filter(**filter_kwargs)
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({
                    'message': 'Invalid field name',
                    'status': status.HTTP_400_BAD_REQUEST
                })
        except FieldDoesNotExist:
            return Response({
                'message': 'Field does not exist',
                'status': status.HTTP_400_BAD_REQUEST
            })
        






class GetOrganizationsByLocation(generics.ListAPIView):
    serializer_class = OrganizationSerializer4
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category_id = self.request.query_params.get('category_id')
        sub_category_id = self.request.query_params.get('sub_category_id')

        if not input_value and not category_id and not sub_category_id:
            raise ValidationError("At least one of 'input_value', 'category_id', or 'sub_category_id' is required.")

        # Start with all organizations
        queryset = Organization.objects.all()

        # Apply input_value filter if provided
        if input_value:
            continent_query = Q(object_id__state__country__continent__pk=input_value)
            country_query = Q(object_id__state__country__pk=input_value)
            state_query = Q(object_id__state__pk=input_value)
            district_query = Q(object_id__pk=input_value)

            combined_query = continent_query | country_query | state_query | district_query
            queryset = queryset.filter(combined_query)

            if not queryset.exists():
                queryset = Organization.objects.filter(object_id=input_value)

        # Apply category_id or sub_category_id filter
        if category_id:
            queryset = queryset.filter(Q(category_id=category_id) | Q(sub_category_id=category_id))

        # Apply sub_category_id filter if provided
        if sub_category_id:
            queryset = queryset.filter(sub_category_id=sub_category_id)

        # Order queryset by _id to avoid pagination warning
        queryset = queryset.order_by('_id')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
