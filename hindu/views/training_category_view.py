from rest_framework import viewsets, generics
from ..models import TrainingCategory
from ..serializers.training_category_serializers import TrainingCategorySerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated




class TrainingCategoryView(viewsets.ModelViewSet):
    queryset = TrainingCategory.objects.all()
    serializer_class = TrainingCategorySerializer
    permission_classes = []

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def list(self, request):
        filter_kwargs = {key: value for key, value in request.query_params.items()}

        try:
            queryset = TrainingCategory.objects.filter(**filter_kwargs)
            
            if not queryset.exists():
                return Response({
                    'message': 'Data not found',
                    'status': 404
                }, status=404)

            serialized_data = TrainingCategorySerializer(queryset, many=True)
            return Response(serialized_data.data)

        except TrainingCategory.DoesNotExist:
            return Response({
                'message': 'Objects not found',
                'status': 404
            }, status=404)