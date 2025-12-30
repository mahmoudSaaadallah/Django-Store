from decimal import Decimal
from rest_framework import serializers
from .models import Collection, Product, Review, Cart, CartItem, Customer



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

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField(method_name='calculate_price')
    product = SimpleProductSerializer(read_only=True)
    def calculate_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price']

class AddingItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No products with the given ID!')
        return value

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('The quantity must be more than zero!')
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id'] 
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdatingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity']
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price', read_only=True)

    def calculate_total_price(self, cart):
        total = 0
        for item in cart.items.all():
            total += item.quantity * item.product.unit_price
        return total
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone',  'birth_date', 'membership']