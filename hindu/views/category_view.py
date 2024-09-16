from rest_framework import viewsets, generics
from ..models import Category,SubCategory

from ..serializers.category_serializer import CategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        # Get the Category by ID
        category = self.get_object()

        # Get all SubCategories related to this Category
        subcategories = SubCategory.objects.filter(category_id=category)

        # Create a list of dictionaries with '_id' and 'name' as keys
        subcategory_data = [{"_id": subcategory._id, "name": subcategory.name} for subcategory in subcategories]

        # Return the list of SubCategory data in the response
        return Response(subcategory_data)