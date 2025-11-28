from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from store.models import Product, OrderItem, Order

# Create your views here.
def hello(request):
    # This will return a query set that will be lazy loaded as it will not hit the database unitl we use the query set for example in a loop or adding any imeidate function like .first()
    # query_set = Product.objects.all()

    # When using get this ORM Request will hit the database imediatly and will return a single object which has the pk = 1;
    # we have to know that when using .get() method if there is no record in the database with pk = 1 it will throw an expception with nonexitist, so we have to hande this inside try and catch.
    #product = Product.objects.get(pk=1)
    try:
        product = Product.objects.get(pk = 1)
    except ObjectDoesNotExist:
        pass
    
    # In the other soluation for the the thrown execption that .get() method will throw if the object doesn't exist is to use .filter() with .first() 
    # .filter() will not hit the database immedatily but, we will add .first() to make sure that this request will work immedatly 
    # .filter() will return an array of objects and if the array is empty the .first() will return none.
    product   = Product.objects.filter(pk = 1).first()
    # This request is more faster than the .get() request.

    # queryset = Product.objects.order_by('-title')
    # queryset = OrderItem.objects.values('product__title').order_by('product__title').distinct()
    # queryset = Product.objects.values('title', 'unit_price')

    # Also we could use .only() to get specific fields from the database.
    # queryset = Product.objects.only('title', 'unit_price')

    # .defer() is the method that will return all the columns except the one that we want to exclude.
    # queryset = Product.objects.defer('description')

    # If we want to get the collection of a product and used 
    # queryset = Product.objects.all()
    # then try to access the collection as a field of the product object.
    # queryset.first().collection.title
    # This will lead to N + 1 Problem as it will hit the data base with new query with each product.

    # To avoid this problem we can use .select_related() method.
    # queryset = Product.objects.select_related('collection').all()
    # This will hit the database only once using the inner join to make sure that the collection table has been fetched.
    # The select_related is used with one to one field or one to many relation

    # But if we have a many to many relation then we have to use .prefetch_related() method.
    # queryset = Product.objects.prefetch_related('promotion').all()
    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('placed_at')[-5:]


    # Aggregate Functions
    # If we use Aggregate function then this will hit the database immedatily.
    # restult = Product.objects.aggregate(count= Count('id'), max_price = Max('unit_price'), min_price = Min('unit_price'), avg_price = Avg('unit_price'))

    # Also we could use these aggregate functions with filter to make this Aggratation work for specific state
    # For example let's get the count of the products that have been ordered more than 4 times
    # result = Product.objects.filter(orderitem__quantity__gt = 4).aggregate(count = Count('id'))
    
    # The max and min price of the products that has collection with id = 3
    result = Product.objects.filter(collection_id = 3).aggregate(max_price = Max('unit_price'), min_price = Min('unit_price'))
    return render(request, 'hello.html', {'result':result})