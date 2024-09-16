from rest_framework import serializers
from ..models import Organization
from ..utils import image_path_to_binary



class OrgnisationSerializer(serializers.ModelSerializer):
    org_images = serializers.SerializerMethodField()
    org_logo = serializers.SerializerMethodField()
    govt_id_proof = serializers.SerializerMethodField()  

    def get_org_images(self, instance):
        filename = instance.org_images
        if filename:
            format = image_path_to_binary(filename)
            return format
        return []

    def get_org_logo(self, instance):
        filename = instance.org_logo
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    def get_govt_id_proof(self, instance):
        filename = instance.govt_id_proof
        if filename:
            format = image_path_to_binary(filename)
            return format
        return None

    class Meta:
        model = Organization
        fields = '__all__'
    


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fields to check for empty or null values
        fields_to_check = ['org_images', 'org_logo', 'chairman', 'web_url', 'est_by','reg_id','est_date','location','organization_name','web_url','org_detail','geo_site','organization_members','sub_category_id','object_id','govt_id_proof']
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null','-']:
                representation[field] = "data not found"
  
        return representation



       
    class Meta:
        model = Organization
        fields = "__all__"



    
    
class OrgnisationSerializer1(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = "__all__"



class OrgnisationSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        fields = ['status']        








class OrganizationSerializer4(serializers.ModelSerializer):
    org_logo = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['_id', 'organization_name', 'org_logo', 'chairman', 'web_url', 'reg_id','est_by','mission','org_detail','desc','object_id','sub_category_id','category_id']

    def get_org_logo(self, obj):
        if obj.org_logo:
            return image_path_to_binary(obj.org_logo)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Fields to check for empty or null values
        fields_to_check = [
             'org_logo', 'chairman', 'web_url',  'reg_id', 
             'organization_name', 'web_url','desc','org_detail','desc','est_by'
           
        ]
        
        # Set a default value of "data not found" for empty or unwanted values
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null', '-']:
                representation[field] = "data not found"
        
        return representation







class OrganizationSerializer5(serializers.ModelSerializer):
    org_logo = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ['_id', 'organization_name', 'org_logo', 'chairman', 'web_url', 'reg_id','est_by','mission','org_detail','desc']

    def get_org_logo(self, obj):
        if obj.org_logo:
            return image_path_to_binary(obj.org_logo)
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Fields to check for empty or null values
        fields_to_check = [
             'org_logo', 'chairman', 'web_url',  'reg_id', 
             'organization_name', 'web_url','desc','org_detail','desc','est_by'
           
        ]
        
        # Set a default value of "data not found" for empty or unwanted values
        for field in fields_to_check:
            if representation.get(field) in [None, '', 'null', '-']:
                representation[field] = "data not found"
        
        return representation

 

class OrganizationSerializer6(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['_id','organization_name','org_logo']        



