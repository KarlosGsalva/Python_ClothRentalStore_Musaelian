import uuid

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Customers(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)
    is_lender = models.BooleanField(default=False)
    is_renter = models.BooleanField(default=True)
    date_update = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    class Meta:
        db_table = 'customers'
        verbose_name = 'customers'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'categories'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class ClothingItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cloth_images/', blank=True, null=True)

    class Meta:
        db_table = 'clothingItems'
        verbose_name = 'clothingItems'
        verbose_name_plural = 'clothingItems'

    def __str__(self):
        return self.title


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    author = models.ForeignKey(Customers, on_delete=models.CASCADE)
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'listings'
        verbose_name = 'listings'
        verbose_name_plural = 'listings'

    def __str__(self):
        return self.title


class RentalRequest(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rentalrequests'
        verbose_name = 'rentalrequests'
        verbose_name_plural = 'rentalrequests'

    def __str__(self):
        return f"Request for {self.listing.title} by {self.customer.username}"


class Transaction(models.Model):
    rental_request = models.ForeignKey(RentalRequest, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_period = models.PositiveIntegerField(help_text="Rental period in days")

    class Meta:
        db_table = 'transactions'
        verbose_name = 'transactions'
        verbose_name_plural = 'transactions'

    def __str__(self):
        return f"Transaction for {self.rental_request.listing.title} on {self.transaction_date}"


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'reviews'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f"Review for {self.listing.title} by {self.customer.username}"