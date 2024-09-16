# from rest_framework import serializers
# from .models import organization,Country,continents
# from .utils import image_path_to_binary


# class OrgnisationSerializer(serializers.ModelSerializer):
#     org_images=serializers.SerializerMethodField()
#     def get_org_images(self, instance):
#             filename = instance.org_images
#             if filename:
#                 format= image_path_to_binary(filename)
#                 # print(format,"******************")
#                 return format
#             return[]
#     class Meta:
#         model = organization
#         fields = "__all__"

# class OrgnisationSerializer1(serializers.ModelSerializer):
    
#     class Meta:
#         model = organization
#         fields = "__all__"


# class countrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = "__all__"


# class continentsSerializer(serializers.ModelSerializer):
#     #  country=serializers.SerializerMethodField()
#     #  def get_country(self,instance):
#     #       country=instance.country
#     #       return{
               
#     #            'name':country.name

#         #   } 
#      class Meta:
#           model=continents
#           fields="__all__"