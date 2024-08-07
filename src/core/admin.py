from django.contrib import admin
from .models import Customers, Category, ClothingItem, Transaction, Review, RentalRequest, Listing

admin.site.register(Customers)
admin.site.register(Category)
admin.site.register(ClothingItem)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(RentalRequest)
admin.site.register(Listing)
