from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.address}-{self.id}'


class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True,
                                 related_name="category_product")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    detail = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    price = models.FloatField()
    demo_url = models.URLField(null=True, blank=True)
    product_file = models.FileField(upload_to='product_files/', null=True)
    download = models.CharField(max_length=200, default=0, null=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        tag_list = self.tags.split(',')
        return tag_list


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.PositiveBigIntegerField()

    def __str__(self):
        return self.user.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer.mobile)

    @property
    def get_order_items(self):
        return self.order_items.all()


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.product.title


class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_addresses")
    address = models.TextField()
    default_address = models.BooleanField(default=False)

    def __str__(self):
        return self.address


class ProductRating(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="rating_customers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ratings')
    rating = models.IntegerField()
    review = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}-{self.review}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to='product_img', null=True)

    def __str__(self):
        return str(self.image)


class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)