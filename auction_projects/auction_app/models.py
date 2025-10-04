from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('seller', 'Seller'),
    ('buyer', 'Buyer')
    )
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return f'{self.username}, {self.role}'


class Brand(models.Model):
    brand_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.brand_name}'


class ModelCar(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    model_car_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.brand}, {self.model_car_name}'


class Car(models.Model):
    FUEL_TYPE = (
    ('diesel', 'Diesel'),
    ('petrol', 'Petrol'),
    ('gas', 'GAS'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid')
    )
    fuel_type = models.CharField(max_length=56, choices=FUEL_TYPE)
    TRANSMISSION_TYPE = (
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
    ('variator', 'Variator')
    )
    model_car = models.ForeignKey(ModelCar, on_delete=models.CASCADE, related_name='cars')
    transmission = models.CharField(max_length=64, choices=TRANSMISSION_TYPE)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2050)])
    mileage = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='cars')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.fuel_type}, {self.transmission}, {self.year}, {self.price}'


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images_cars', blank=True, null=True)

    def __str__(self):
        return f'{self.car}'


class Auction(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='auction')
    start_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    STATUS_CHOICES = (
    ('active', 'Active'),
    ('done', 'Done'),
    ('cancelled', 'Cancelled')
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.car}, {self.status}'


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bid_buyers')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.amount}, {self.buyer}, {self.auction}'


class Feedback(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='seller_user')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buyers_user')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.seller}, {self.buyer}, {self.rating}, {self.comment}'






