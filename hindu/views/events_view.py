from rest_framework import viewsets,generics
from ..models import Events
from ..serializers import *
from ..models import Organization, Country,Continent,Register,District,Events
from rest_framework import status
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from ..utils import save_image_to_folder
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from ..enums import EventStatusEnum
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, pagination
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField, ExpressionWrapper





class CustomPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100




class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer1
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    def list(self, request):
    # Extract query parameters for filtering
        for event in Events.objects.all():
            event.update_event_status()
        filter_kwargs = request.query_params.dict()

        # Get the queryset filtered by the provided query parameters
        queryset = Events.objects.filter(**filter_kwargs)

        # If no results found
        if not queryset.exists():
            return Response({
                'message': 'Data not found',
                'status': 404
            }, status=status.HTTP_404_NOT_FOUND)

        # Filter events based on their status
        upcoming_events = queryset.filter(event_status="UPCOMING").order_by('start_date')
        completed_events = queryset.filter(event_status="COMPLETED").order_by('start_date')

        # Serialize both upcoming and completed events
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)

        # Return the formatted response
        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })


    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
        except Events.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            username = request.user.username
            register_instance = Register.objects.get(username=username)
            is_member = register_instance.is_member

            if is_member == "FALSE":
                return Response({
                    "message": "Cannot create event. Membership details are required. Update your profile and become a member."
                }, status=status.HTTP_400_BAD_REQUEST)

            created_at = timezone.now()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            brochure = request.data.get('brochure')
            if brochure and brochure != "null":
                saved_brochure_location = save_image_to_folder(brochure, serializer.instance._id, serializer.instance.name, 'eventbrochures')
                if saved_brochure_location:
                    serializer.instance.brochure = saved_brochure_location

            event_images = request.data.get('event_images', [])
            if event_images:
                saved_event_image_paths = []
                for image_data in event_images:
                    if image_data and image_data != "null":
                        saved_location = save_image_to_folder(image_data, serializer.instance._id, serializer.instance.name, 'hinduworldevents')
                        if saved_location:
                            saved_event_image_paths.append(saved_location)
                serializer.instance.event_images = saved_event_image_paths
                serializer.instance.save()

            send_mail(
                'New Event Added',
                f'User ID: {request.user.id}\n'
                f'Contact Number: {register_instance.contact_number}\n'
                f'Full Name: {request.user.get_full_name()}\n'
                f'Created Time: {created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
                f'Event ID: {serializer.instance._id}\n'
                f'Event Name: {serializer.instance.name}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            return Response({
                "message": "Event added successfully.",
                "result": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Register.DoesNotExist:
            return Response({
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "message": "An error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_instance = serializer.save()
            return Response({
                "message": "Updated successfully",
                "data": self.get_serializer(updated_instance).data
            }, status=status.HTTP_200_OK)
        except Events.DoesNotExist:
            return Response({'message': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)







class UpdateEventStatus(generics.GenericAPIView):
    serializer_class = EventSerializer2

    def put(self, request, event_id):
        try:
            event = Events.objects.get(pk=event_id, status='PENDING')
        except Events.DoesNotExist:
            return Response({
                'message': 'Event with PENDING status not found for the provided ID'
            }, status=status.HTTP_404_NOT_FOUND)

        # Update the status to 'SUCCESS'
        event.status = 'SUCCESS'
        event.save()

        # Serialize the updated event
        serializer = self.get_serializer(event)

        return Response({
            'message': 'success',
            'result': serializer.data
        }, status=status.HTTP_200_OK)








 









class GetEventsByLocation(generics.ListAPIView):
    serializer_class = EventsSerializer1
    pagination_class = CustomPagination

    def get_queryset(self):
        input_value = self.request.query_params.get('input_value')
        category = self.request.query_params.get('category')

        if not input_value and not category:
            raise ValidationError("At least one of input_value or category must be provided.")

        today = timezone.now().date()

        # Define queries for each location level
        continent_query = Q(object_id__state__country__continent__pk=input_value)
        country_query = Q(object_id__state__country__pk=input_value)
        state_query = Q(object_id__state__pk=input_value)
        district_query = Q(object_id__pk=input_value)

        # Combine location queries with OR operator
        combined_query = Q()
        if input_value:
            combined_query |= continent_query | country_query | state_query | district_query

        # Apply category filter if provided
        if category:
            combined_query &= Q(category=category)

        # Filter by combined query and order by proximity to today's date
        queryset = Events.objects.filter(combined_query).select_related(
            'object_id__state__country__continent',
            'object_id__state__country',
            'object_id__state',
            'object_id'
        ).order_by(
            Case(
                When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                When(start_date__lt=today, then=Value(1)),   # Past events
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'
        )

        # Check if queryset is empty and filter directly by object_id
        if not queryset.exists() and input_value:
            queryset = Events.objects.filter(object_id=input_value)
            if category:
                queryset = queryset.filter(category=category)

            # Reorder by proximity to today's date and start date
            queryset = queryset.order_by(
                Case(
                    When(start_date__gte=today, then=Value(0)),  # Upcoming or today
                    When(start_date__lt=today, then=Value(1)),   # Past events
                    default=Value(2),
                    output_field=IntegerField()
                ),
                'start_date'
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter for upcoming and completed events
        today = timezone.now().date()
        upcoming_events = queryset.filter(start_date__gte=today)
        completed_events = queryset.filter(start_date__lt=today)

        # Paginate the upcoming events
        page = self.paginate_queryset(upcoming_events)
        if page is not None:
            event_upcoming_serializer = self.get_serializer(page, many=True)
            event_completed_serializer = self.get_serializer(completed_events, many=True)

            return Response({
                "status": 200,
                "event_upcoming": event_upcoming_serializer.data,
                "event_completed": event_completed_serializer.data,
            })

        # If no pagination, return all events
        event_upcoming_serializer = self.get_serializer(upcoming_events, many=True)
        event_completed_serializer = self.get_serializer(completed_events, many=True)

        return Response({
            "status": 200,
            "event_upcoming": event_upcoming_serializer.data,
            "event_completed": event_completed_serializer.data,
        })









class EventstatusView(generics.ListAPIView):
    serializer_class = EventsSerializer4
    pagination_class = CustomPagination

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        now = timezone.now()

        queryset = Events.objects.all()

        # Update event statuses before returning the queryset
        for event in queryset:
            event.update_event_status()

        if status_param:
            if status_param not in dict(EventStatusEnum.__members__).keys():
                raise ValidationError("Invalid status value")
            queryset = queryset.filter(event_status=status_param)

        # Order events: upcoming events first, then completed events
        return queryset.order_by(
            Case(
                When(event_status=EventStatusEnum.UPCOMING.name, then=Value(0)),
                When(event_status=EventStatusEnum.COMPLETED.name, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            ),
            'start_date'  # Further order by start date within each status group
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)