

from rest_framework import serializers
from ..models import *
from ..utils import image_path_to_binary


class EventCategorySerializer(serializers.ModelSerializer):
    pic = serializers.SerializerMethodField()
    def get_pic(self, instance):

            filename = instance.pic
            if filename:
                format= image_path_to_binary(filename)
                # print(format,"******************")
                return format
            return None

    class Meta:
        model = EventCategory
        fields = ("__all__")