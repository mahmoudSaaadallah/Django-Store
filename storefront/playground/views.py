from django.db.models.aggregates import Count, Max, Min, Avg
from django.db.models import Q, F, Value, ExpressionWrapper
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import DecimalField
from django.shortcuts import render
from store.models import Collection, Product, OrderItem, Order

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
    # result = Product.objects.filter(collection_id = 3).aggregate(max_price = Max('unit_price'), min_price = Min('unit_price'))

    # ex = ExpressionWrapper(F('unit_price') * 0.8, output_field = DecimalField())
    # result = Product.objects.annotate(discount = ex)



    # Create New Object and save it to the database
    # collection = Collection()
    # collection.title = 'Winter Sale'
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # This is the first way to add new object to the database be providing the values to variables of the object.

    # The second way is by using .create()
    # Collection.objects.create(title='Winter Sale', featured_product_id=1)
    # This way also will save the object to the database.


    # Update data
    # To update a record in the database we have first specify this record using pk 
    # collection = Collection(pk = 1)
    # This line of code will allow us to deal with the Collection recorde with Pk=1 
    # Now we could change the data that we want then save the object again to the database
    # collection.title = 'Updated Title'
    # collection.featured_product = None
    # collection.save()
    # Now we have to know that this type of update is a fully update which mean we have to update all the fields for the record 
    # If we missed a field with no updates this field will take the default value, which mean it not like partail update 
    # So if we want to update specific field from a record from the database we can't use this way 

    # Instead we have to use feach the object first from the database then update the field that we want
    # collection = Collection.objects.get(pk=1)
    # fetching the object from the database will get the values to the field so when we call the .save() the fields that didn't changed 
    # will keep its value.
    # collection.featured_product = Product(pk=3)
    # collection.save
    # here we didn't update the title so the collection title will keep the title that stored in the database.
    # This is how we apply the partial update.

    # If we want to avoid fetching the record form the database to reduce the memory useage then we could use .update() method which 
    # work with fully update if we provide all the fields or partial update if we provide only specific filed.
    #Collection.objects.filter(pk=1).update(title="New Title")
    # we have to know that without using .filter() with specific condition we will update all the column in the database for all the records.
    # So if we want to update only one record then we have to use .filter() to specify this record it's exactly like using where contation
    # with update statement in SQL.

    return render(request, 'hello.html', {'result':result}) 