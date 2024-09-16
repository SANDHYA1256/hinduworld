from rest_framework import serializers
from ..models import Training,Register
from ..utils import image_path_to_binary,video_path_to_binary

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = "__all__"



class TrainingSerializer2(serializers.ModelSerializer):
    
    class Meta:
        model = Training
        fields = ['status']        







class TrainerSerializer3(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    certificate = serializers.SerializerMethodField()

    class Meta:
        model = Register
        fields = ["full_name", "image", "video", "map_location", "status", "experience", "certificate", "achievements", "user_type", "training_type", "email", "contact_number"]

    def get_image(self, obj):
        if obj.image:
            encoded_image = image_path_to_binary(obj.image)
            return encoded_image if encoded_image else None
        return None

    def get_video(self, obj):
        if obj.video:
            encoded_video = video_path_to_binary(obj.video)
            return encoded_video if encoded_video else None
        return None

    def get_certificate(self, obj):
        if obj.certificate:
            encoded_certificate = image_path_to_binary(obj.certificate)
            return encoded_certificate if encoded_certificate else None
        return None
    




class TrainingSerializer4(serializers.ModelSerializer):
                    
    class Meta:
        model = Training
        fields = ['_id','name','image']     





class TrainingSerializer5(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Training
        fields = ['_id', 'name', 'desc', 'image', 'location','start_date','end_date','start_time','end_time','trainer_name','contact_details','video','training_type','category','object_id']  

    def get_image(self, obj):
        if obj.image:
            encoded_image = image_path_to_binary(obj.image)
            return encoded_image if encoded_image else None
        return None

    def get_video(self, obj):
        if obj.video:
            encoded_video = video_path_to_binary(obj.video)
            return encoded_video if encoded_video else None
        return None
