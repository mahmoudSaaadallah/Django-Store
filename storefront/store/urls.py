from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('reviews', views.ReviewViewSet)

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='poruct-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('products/<int:product_pk>/', include(router.urls)),
    path('collections/', views.CollectionList.as_view(), name='collection-list'), 
    path('collection/<int:pk>', views.CollectionDetail.as_view(), name='collection-detail'),
]
