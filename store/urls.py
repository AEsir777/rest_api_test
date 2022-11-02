from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import store.views
import store.api_views

urlpatterns = [
    path('api/example1', store.api_views.ProductListAPIView.as_view(), name='api-list'),
    path('api/example1/new', store.api_views.ProductCreateAPIView.as_view(), name='api-create'),
    path('api/example1/<int:id>/rud', store.api_views.ProductRUDAPIView.as_view(), name='api-rud'),
    path('api/example1/<int:id>/stat', store.api_views.ProductStatsAPIView.as_view(), name='api-stat'),
    path('products/<int:id>/', store.views.show, name='show-product'),
    path('cart/', store.views.cart, name='shopping-cart'),
    path('', store.views.index, name='list-products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)