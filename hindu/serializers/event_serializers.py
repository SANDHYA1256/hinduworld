from rest_framework import serializers
from ..models import Events
from ..utils import image_path_to_binary

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"






class EventsSerializer1(serializers.ModelSerializer):
    brochure = serializers.SerializerMethodField()
    event_images = serializers.SerializerMethodField()  
    relative_time = serializers.SerializerMethodField()


    def get_brochure(self, instance):
        if instance.brochure:
            return image_path_to_binary(instance.brochure)
        return None

    def get_event_images(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None
    
    def get_relative_time(self, obj):
        return obj.relative_time

    class Meta:
        model = Events
        fields = '__all__'






class EventSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Events
        fields = ['status']        







class EventsSerializer3(serializers.ModelSerializer):
    event_image = serializers.SerializerMethodField()  # Renaming to event_image for single image

    def get_event_image(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None

    class Meta:
        model = Events
        fields = ['_id', 'event_image', 'name']




class EventsSerializer4(serializers.ModelSerializer):
    relative_time = serializers.SerializerMethodField()
    event_images = serializers.SerializerMethodField()  # Changed to event_image for a single image

    def get_event_images(self, instance):
        # Return only the first image if available
        if instance.event_images:
            first_image = instance.event_images[0] if instance.event_images else None
            return image_path_to_binary(first_image) if first_image else None
        return None



    class Meta:
        model = Events
        fields = ['_id', 'name', 'start_date', 'start_time','end_date', 'relative_time', 'event_status','event_images','organization','object_id','category']

    def get_relative_time(self, obj):
        return obj.relative_time