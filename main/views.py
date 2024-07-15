from django.shortcuts import render, get_object_or_404
from . import serializers, models
from rest_framework import generics, permissions, viewsets
from .permissions import IsOwnerOrReadOnly


# Create your views here.

class VendorList(generics.ListAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VendorCreateList(generics.CreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VendorDetail(generics.RetrieveAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]


class VendorUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class ProductCreateList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all().select_related('category', 'vendor')
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if 'category' in self.request.GET:
            category = self.request.GET['category']
            category = models.ProductCategory.objects.get(id=category)
            qs = qs.filter(category=category)
            return qs

    def perform_create(self, serializer):
        vendor = models.Vendor.objects.filter(user=self.request.user).select_related('user').first()
        serializer.save(vendor=vendor)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all().select_related('category', 'vendor')
    serializer_class = serializers.ProductSerializer

    def perform_update(self, serializer):
        vendor = models.Vendor.objects.filter(user=self.request.user).select_related('user').first()
        serializer.save(vendor=vendor)


class TagProductCreateList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all().select_related('category', 'vendor')
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tag = self.request.GET['tag']
        qs = qs.filter(tags__icontains=tag)
        return qs


class RelatedProductCreateList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all().select_related('category', 'vendor')
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        product_id = self.kwargs['pk']
        product = models.Product.objects.get(id=product_id)
        qs = qs.filter(category=product.category).exclude(id=product_id)
        return qs


class CustomerList(generics.ListAPIView):
    queryset = models.Customer.objects.all().select_related('user')
    serializer_class = serializers.CustomerSerializer


class CustomerCreateList(generics.CreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all().select_related('user')
    serializer_class = serializers.CustomerSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all().select_related('customer')
    serializer_class = serializers.OrderSerializer
    #
    # def perform_create(self, serializer):
    #     customer = models.Customer.objects.filter(user=self.request.user).select_related('user').last()
    #     serializer.save(cutomer=customer)


# class OrderCreateList(generics.CreateAPIView):
#     queryset = models.Order.objects.all().select_related('customer')
#     serializer_class = serializers.OrderSerializer
#
#     def perform_create(self, serializer):
#         customer = models.Customer.objects.filter(user=self.request.user).select_related('user').last()
#         serializer.save(cutomer=customer)

class OrderItemList(generics.ListCreateAPIView):
    queryset = models.OrderItems.objects.all().select_related('product')
    serializer_class = serializers.OrderItemSerializer


class CustomerOrderItemList(generics.ListCreateAPIView):
    queryset = models.OrderItems.objects.all().select_related('product')
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        customer_id = self.kwargs['pk']
        qs = qs.filter(order__customer__id=customer_id)
        return qs


class OrderDetailView(generics.ListAPIView):
    # queryset = models.OrderItems.objects.all().select_related('order', 'product')
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id = self.kwargs['pk']
        order = get_object_or_404(models.Order, id=order_id)
        order_items = models.OrderItems.objects.filter(order=order).select_related("order", 'product')
        return order_items


# class OrderDetailView(generics.RetrieveAPIView):
#     queryset = models.Order.objects.all().select_related('customer')
#     serializer_class = serializers.OrderDetailSerializer


class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerAddress.objects.all().select_related('customer')
    serializer_class = serializers.CustomerAddressSerializer


class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = models.ProductRating.objects.all().select_related('customer', 'product')
    serializer_class = serializers.ProductRatingSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer


class WishListView(generics.ListCreateAPIView):
    queryset = models.WishList.objects.all()
    serializer_class = serializers.WishListSerializer

