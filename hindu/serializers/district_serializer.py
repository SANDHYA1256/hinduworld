from rest_framework import serializers
from ..models import District
from ..utils import image_path_to_binary


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = "__all__"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['headquarters', 'name', 'shortname', 'desc', 'cityname','type','state','created_at']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation

      

