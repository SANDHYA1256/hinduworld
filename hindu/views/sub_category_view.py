from rest_framework import viewsets, generics
from ..models import SubCategory
from ..serializers.sub_category_serializer import SubCategorySerializer


class SubCategoryView(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer