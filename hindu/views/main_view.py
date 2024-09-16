from rest_framework.views import APIView, status
from rest_framework.response import Response
from ..serializers import *
from ..models.district import District
from ..models.event import Events
from ..models.event_category import EventCategory
from ..models.organization import Organization 
from ..models.training import Training  
from ..utils import image_path_to_binary


class OrganizationMain(APIView):
    def get(self, request):
        organizations = Organization.objects.all()[:4]  # Retrieve the first 4 organizations globally
        organization_serializer = OrgnisationSerializer1(organizations, many=True)
        
        # Convert organization images and logos to base64
        for org in organization_serializer.data:
            # Convert org_images to base64
            if 'org_images' in org and org['org_images']:
                org['org_images'] = image_path_to_binary(org['org_images'])
            
            # Convert org_logo to base64
            if 'org_logo' in org and org['org_logo']:
                org['org_logo'] = image_path_to_binary(org['org_logo'])
        
        return Response({
            'organizations': organization_serializer.data,
        })


class EventsMain(APIView):
    def get(self, request):
        events = Events.objects.all()[:4]  # Retrieve the first 4 events globally
        events_serializer = EventsSerializer3(events, many=True)

        return Response({
            'events': events_serializer.data,
        })
    

class TrainingMain(APIView):
    def get(self, request):
        trainings = Training.objects.all()[:4]  # Retrieve the first 4 trainings globally
        training_serializer = TrainingSerializer4(trainings, many=True)
        
        # Convert images and videos to base64
        for training in training_serializer.data:
            if 'image' in training and training['image']:
                training['image'] = image_path_to_binary(training['image'])

            
        return Response({
            'trainings': training_serializer.data,
        })