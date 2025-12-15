from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='poruct-list'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('collections/', views.collection_list, name='collection-list'), 
]
