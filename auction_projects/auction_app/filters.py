from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter
from .models import Car

class CarFilter(FilterSet):
    brand = CharFilter(field_name='model_car__brand__brand_name', lookup_expr='icontains')
    model = CharFilter(field_name='model_car__model_car_name', lookup_expr='icontains')
    year = NumberFilter(field_name='year')
    fuel_type = CharFilter(field_name='fuel_type', lookup_expr='iexact')
    transmission = CharFilter(field_name='transmission', lookup_expr='iexact')
    price_min = NumberFilter(field_name='price', lookup_expr='gte')
    price_max = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'fuel_type', 'transmission', 'price_min', 'price_max']
