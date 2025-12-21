from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product, Review



class CollectionSerializer(serializers.ModelSerializer):
    # products_count = serializers.SerializerMethodField('get_products_count')
    # def get_products_count(self, collection):
    #     return collection.product_set.count()

    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

class ProductSerializer(serializers.ModelSerializer):
    # we could add a new attribute that doesn't exist in the Product model like
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax')
    # Here we created a new attribute with type of serializerMethod which mean it accept a method that is responsabile for getting its vale.

    # Also we could add a related field by different ways
    # if we want to ge the id for the collection we could use
    # collection = serializers.PrimaryKeyRelatedField( 
    #     queryset = Collection.objects.all()
    # )
    # but if we want to represent the string then we could use
    # collection = serializers.StringRelatedField()
    # here we have to know that without using select_related('collection') in the views.py 
    # this will case N + 1 problem.

    # Ther is another way to add a related field, like if we want to return an object of the collection then we could use
    # collection = CollectionSerializer()
     
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection','slug', 'inventory']
    def calculate_price_with_tax(self, product):
        # Here we used Decimal Class as we can't mulitply float with decimla as the unit_price is decimal and 1.14 is float then 
        # we can't mulitply them so we have to convert 1.14 to decimal before appling the operation.
        # Also we used round to round the result to only two degits.
        return round(product.unit_price * Decimal(1.14),2)
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
