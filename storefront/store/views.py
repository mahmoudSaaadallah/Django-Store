from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
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
from .filters import ProductFilter
from django.db.models import Q
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    # As we are going to use the collection_id as a params in the url then we can't override the queryset parameter we have to override the get_queryset function.
    # we have to know that with the following get_queryset we will filter only with collection_id not anything else.
    # but if we want to filter with other parameters then we have to specify it in the get_queryset method and that will make the function 
    # complicated, on the othe hand we could use genereic filter.
    # generic filter could be appied using django-filter package.
    # def get_queryset(self):
    #     queryset = Product.objects.select_related('collection').all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    # so instead of override the get_query set to add filters we could use django-filter as the following.
    # here we add the searchfilter class to use it search about the product
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']


    # we could make manual search by override the get_queryset function as following.
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search_query = self.request.query_params.get('q')
    #     if search_query:
    #         search_fields = ['title', 'description', 'collection__title']
    #         for field in search_fields:
    #             query = Q(title__icontains=search_query) | Q(description__icontains=search_query)
    #         queryset = queryset.filter(query)
    #     return queryset
        
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

    