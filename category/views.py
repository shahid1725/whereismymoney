from category.models import Category
from category.serializers import CategorySerializer
from whereismymoney.views import UserOwnedModelViewSet


class CategoryViewSet(UserOwnedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
