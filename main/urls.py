from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('address', views.CustomerAddressViewSet)
router.register('product-rating', views.ProductRatingViewSet)

urlpatterns = [
    path('vendors/', views.VendorList.as_view(), name='vendor-list'),
    path('products/', views.ProductCreateList.as_view(), name='product-list'),
    path('vendors/create/', views.VendorCreateList.as_view(), name='vendor-create'),
    path('vendors/<int:pk>/', views.VendorDetail.as_view(), name='vendor-detail'),
    path('vendors/<int:pk>/update', views.VendorUpdate.as_view(), name='vendor-update'),
    path('products/<int:pk>/update', views.ProductDetail.as_view(), name='product-update'),
    path('related-products/<int:pk>', views.RelatedProductCreateList.as_view(), name='product-related'),
    path('products/<str:tag>', views.TagProductCreateList.as_view(), name='product-tags'),
    # category
    path('category/', views.CategoryListCreateView.as_view(), name="category-list"),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name="category-detail"),

    # customer
    path('customer/', views.CustomerList.as_view(), name='customer-list'),
    path('customer/create/', views.CustomerCreateList.as_view(), name='customer-create'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customer-detail'),
    # Order
    path('order/', views.OrderList.as_view(), name='order-list'),
    path('order-detail/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('customer/<int:pk>/orderitems', views.CustomerOrderItemList.as_view(), name='order-customer'),
    path('orderitems/', views.OrderItemList.as_view(), name='order-items'),
    # path('update-order-status/<int:pk>', views.OrderItemList.as_view(), name='order-status'),
    path('wish-list/', views.WishListView.as_view(), name='wish-list'),

]
urlpatterns += router.urls
