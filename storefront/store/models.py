from django.db import models

# Create your models here.
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title   
    
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotion = models.ManyToManyField(Promotion)

    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['-unit_price']

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'), 
        ('S', 'Silver'),
        ('G', 'Gold'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', "Complete"),
        ('F', 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='P')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.PositiveIntegerField()
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CarItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()