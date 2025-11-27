import django_filters
from .models import Product, ProductVariant

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    min_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='lte')
    size = django_filters.CharFilter(field_name='variants__size', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'size']
