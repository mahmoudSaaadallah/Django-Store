
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', viewset=views.ProductViewSet, basename='products')
router.register('collections', viewset=views.CollectionViewSet)
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
router.register('reviews', views.ReviewViewSet)
router.register('cart', viewset=views.CartViewSet, basename='cart-creation')
router.register('customers', viewset=views.CustomerViewSet, basename='customer')
cart_item_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_item_router.register('items', views.CartItemViewSet, basename='cart-item')
urlpatterns = router.urls + products_router.urls + cart_item_router.urls
