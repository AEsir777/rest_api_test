from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from store.serializers import ProductSerializer
from store.models import Product

class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

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
