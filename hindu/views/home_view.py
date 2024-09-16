from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.organization import Organization
from ..models.event import Events
from ..models.training import Training
from ..serializers import OrganizationSerializer6, EventsSerializer3, TrainingSerializer4
from ..utils import image_path_to_binary

class HomeView(APIView):
    def get(self, request):
        # Retrieve the first 4 organizations globally
        organizations = Organization.objects.all()[:4]
        organization_serializer = OrganizationSerializer6(organizations, many=True)
        
        # Convert organization images and logos to base64
        for org in organization_serializer.data:
            if 'org_images' in org and org['org_images']:
                org['org_images'] = image_path_to_binary(org['org_images'])
            if 'org_logo' in org and org['org_logo']:
                org['org_logo'] = image_path_to_binary(org['org_logo'])

        # Retrieve the first 4 events globally
        events = Events.objects.all()[:4]
        events_serializer = EventsSerializer3(events, many=True)

        # Retrieve the first 4 trainings globally
        trainings = Training.objects.all()[:4]
        training_serializer = TrainingSerializer4(trainings, many=True)
        
        # Convert training images to base64
        for training in training_serializer.data:
            if 'image' in training and training['image']:
                training['image'] = image_path_to_binary(training['image'])

        return Response({
            'organizations': organization_serializer.data,
            'events': events_serializer.data,
            'trainings': training_serializer.data,
        })
