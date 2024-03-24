from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from edusystem.serializers import ProductSerializer, LessonSerializer
from edusystem.models import Product, Lesson, ProductAccess


class ProductListApi(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        products = Product.objects.filter(
            accesses__user=user, accesses__is_valid=True
        ).annotate(lessons_count=Count('lessons')).distinct()
        return products


def user_has_access_for_product(user, product):
    return ProductAccess.objects.filter(user=user, product=product, is_valid=True)


class LessonListApi(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product = self.kwargs['pk']
        user = self.request.user
        if not user_has_access_for_product(user, product):
            raise PermissionError("I have not access, try later")
        return Lesson.objects.filter(product=product)

