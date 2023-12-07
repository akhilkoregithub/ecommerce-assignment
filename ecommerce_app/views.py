from rest_framework.response import Response
from rest_framework import viewsets
from .models import Customer, Product, Order, OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter orders based on products
        products_param = self.request.query_params.get('products')
        if products_param:
            products_list = products_param.split(',')
            queryset = queryset.filter(order_item__product__name__in=products_list).distinct()

        # Filter orders based on customer
        customer_param = self.request.query_params.get('customer')
        if customer_param:
            queryset = queryset.filter(customer__name=customer_param)

        return queryset

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

