from rest_framework import serializers
from . import models


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['id', 'user', 'address']


class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vendor
        fields = ['address']


class VendorDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = models.Vendor
        fields = ['id', 'user', 'address']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCategory
        fields = ['id', 'title', 'detail']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    product_rating = serializers.StringRelatedField(many=True, read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)

    # product_rating = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Product
        fields = ['id', 'category', 'vendor', 'title', 'detail', 'price', 'product_rating', 'product_images',
                  'tag_list', 'product_file', 'download']
        read_only_fields = ['vendor']


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = models.Customer
        fields = ['id', 'user', 'mobile']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ['mobile']


# class OrderItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.OrderItems
#         fields = ['id', 'order', 'product']


class OrderSerializer(serializers.ModelSerializer):
    # customer = serializers.CharField(source='customer.user.username')

    class Meta:
        model = models.Order
        fields = ['id', 'customer', 'order_status', 'order_time']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderItems
        fields = ['id', 'order', 'product', 'qty', 'price']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['order'] = OrderDetailSerializer(instance.order).data
        response['product'] = ProductSerializer(instance.product).data
        return response


class OrderDetailSerializer(serializers.ModelSerializer):
    order = serializers.CharField(source='order.customer')
    product = serializers.CharField(source='product.title')

    class Meta:
        model = models.OrderItems
        fields = ['id', 'order', 'product']


# class OrderDetailSerializer(serializers.ModelSerializer):
#     get_order_items = OrderItemsSerializer(many=True)
#     class Meta:
#         model = models.Order
#         fields = ['get_order_items']


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAddress
        fields = ['id', 'customer', 'address', 'default_address']


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductRating
        fields = ['id', 'customer', 'product', 'review', 'add_time', 'rating']


class WishListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WishList
        fields = ['id', 'product', 'customer']
