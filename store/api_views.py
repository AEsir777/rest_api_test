from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from store.serializers import ProductSerializer
from store.models import Product

class ProductsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['id']
    # enable full text search
    search_fields = ['name', 'description']
    # enable pagination
    pagination_class = ProductsPagination

    # filter with more complex field
    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale')
        if on_sale is None:
            return super().get_queryset()
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return self.queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        return self.queryset

class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0.0:
                raise ValidationError({ 'price': 'Must be positive' })
        except ValueError:
            raise ValidationError({ 'price': 'A valid number is required' })
        return super().create(request, *args, **kwargs)


""" class ProductDestroyAPIView(DestroyAPIView):
    serializer_class = Pr
 """