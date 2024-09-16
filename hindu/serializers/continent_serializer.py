from rest_framework import serializers
from ..models import Continent

class continentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('overall_population') is None:
            representation['overall_population'] = '0'
        return representation
