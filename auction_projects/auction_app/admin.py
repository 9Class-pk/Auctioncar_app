import nested_admin.nested
from django.contrib import admin
from .models import UserProfile, Brand, ModelCar, Car, CarImage, Auction, Bid, Feedback

admin.site.register(UserProfile)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Feedback)


class CarImageInline(nested_admin.nested.NestedTabularInline):
     model = CarImage
     extra = 1



class CarInline(nested_admin.nested.NestedTabularInline):
    model = Car
    extra = 1
    inlines = [CarImageInline]


class ModelCarInline(nested_admin.nested.NestedTabularInline):
    model = ModelCar
    extra = 1
    inlines = [CarInline]


@admin.register(Brand)
class BrandAdmin(nested_admin.nested.NestedModelAdmin):
    inlines = [ModelCarInline]