from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product, Collection, Review
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    def destory(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    def destroy(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection contains products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# class CollectionList(generics.ListCreateAPIView):
#     # Here we inheret from ListCreateAPIView class which inheret from generics class and some other mixinx like(mixins.ListModelMixin, mixins.CreateModelMixin).
#     # generics class inherte from the APIView and this class has some Attributes(queryset, serializer_class).
#     # You'll need to either set these attributes,

#     # queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     # serializer_class = CollectionSerializer

#     # or override `get_queryset()`/`get_serializer_class()`.
#     # If you are overriding a view method, it is important that you call
#     # `get_queryset()` instead of accessing the `queryset` property directly,
#     # as `queryset` will get evaluated only once, and those results are cached
#     # for all subsequent requests.
#     def get_queryset(self):
#         return Collection.objects.annotate(products_count=Count('products')).all()
    
#     def get_serializer_class(self):
#         return CollectionSerializer

            
# class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response({'error': 'Collection contains products'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}
    # def get_queryset(self):
    #     return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    # def perform_create(self, serializer):
    #     product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
    #     serializer.save(product=product)

    