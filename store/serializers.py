from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant

# -------------------
# CATEGORY
# -------------------
class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'product_count']
    
    def get_product_count(self, obj):
        return obj.products.count()


# -------------------
# PRODUCT IMAGES
# -------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_main']


# -------------------
# PRODUCT VARIANTS
# -------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'price', 'inventory_quantity']


# -------------------
# PRODUCTS
# -------------------
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    main_image = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    available_sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'main_image', 'price_range', 'available_sizes', 'created_at']

    def get_main_image(self, obj):
        main = obj.images.filter(is_main=True).first()
        request = self.context.get('request')
        if main and request:
            return request.build_absolute_uri(main.image.url)
        return None

    def get_price_range(self, obj):
        variants = obj.variants.filter(inventory_quantity__gt=0)
        if not variants.exists():
            return None
        prices = variants.values_list('price', flat=True)
        return {"min": min(prices), "max": max(prices)}

    def get_available_sizes(self, obj):
        return list(obj.variants.values_list('size', flat=True).distinct())


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'category', 'images', 'variants', 'created_at']
