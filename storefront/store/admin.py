from django.contrib import admin
from . import models
# Register your models here.

# This is how to register our models in the admin site to enable us to see them in the admin site
# admin.site.register(models.Collection)
# admin.site.register(models.Product)

# To full control the way the admin site looks like we can use the following code
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # The list_display specify the columns that will be displayed when entering the Admin panal for the Products
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']

    # The list_editable prop used to specify the fields that could be edited on the list page.
    list_editable = ['unit_price']

    # The list_per_page specify the number of records that will apear per page.
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        else:
            return 'Ok'
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer__first_name']
    list_select_related = ['customer']
    ordering = ['placed_at']