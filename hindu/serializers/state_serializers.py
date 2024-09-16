from rest_framework import serializers
from ..models import State

class StateSeerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['name', 'shortname', 'desc', 'created_at', 'type','country']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation