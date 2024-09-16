from rest_framework import serializers
from ..models import SubCategory
from ..serializers import CategorySerializer



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['_id','name','category_id','desc']