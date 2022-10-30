from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import store.views

urlpatterns = [
    path('products/<int:id>/', store.views.show, name='show-product'),
    path('cart/', store.views.cart, name='shopping-cart'),
    path('', store.views.index, name='list-products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)