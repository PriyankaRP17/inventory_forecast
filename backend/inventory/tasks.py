from celery import shared_task
from django.core.mail import send_mail
from django.db import models as django_models

from .models import Product


@shared_task
def check_low_stock_and_alert():
    low_stock_products = Product.objects.filter(
        quantity__lte=django_models.F('low_stock_threshold')
    )
    for product in low_stock_products:
        send_low_stock_email.delay(product.id)
    return f"Checked {low_stock_products.count()} low stock products"


@shared_task
def send_low_stock_email(product_id):
    try:
        product = Product.objects.get(id=product_id)
        send_mail(
            subject=f'Low Stock Alert: {product.name}',
            message=(
                f'Product {product.name} (SKU: {product.sku}) '
                f'is running low.\n'
                f'Current quantity: {product.quantity}\n'
                f'Threshold: {product.low_stock_threshold}'
            ),
            from_email='noreply@inventory.com',
            recipient_list=['manager@inventory.com'],
            fail_silently=True,
        )
        return f"Alert sent for {product.name}"
    except Product.DoesNotExist:
        return "Product not found"
