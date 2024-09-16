from rest_framework import serializers
from ..models import Country,organization
from ..utils import image_path_to_binary


class countrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"





class CountrySerializer1(serializers.ModelSerializer):
    image_location = serializers.SerializerMethodField()

    def get_image_location(self, instance):
        filename = instance.image_location
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('overall_population') is None:
            representation['overall_population'] = '0'
        return representation
    
    class Meta:
        model = Country
        fields = "__all__"