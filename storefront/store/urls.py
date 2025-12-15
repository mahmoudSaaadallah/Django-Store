from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='poruct_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
