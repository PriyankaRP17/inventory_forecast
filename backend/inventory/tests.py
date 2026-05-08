import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch

from inventory.models import Category, Product, Supplier, Warehouse

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin', password='admin123', role='admin'
    )


@pytest.fixture
def manager_user():
    return User.objects.create_user(
        username='manager', password='manager123', role='manager'
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        username='staff', password='staff123', role='staff'
    )


@pytest.fixture
def warehouse():
    return Warehouse.objects.create(name='Main Warehouse', location='Chennai')


@pytest.fixture
def category():
    return Category.objects.create(name='Electronics', description='Electronic items')


@pytest.fixture
def supplier():
    return Supplier.objects.create(
        name='Tech Supplies', email='tech@supplier.com', phone='9876543210'
    )


@pytest.fixture
def product(warehouse, category, supplier):
    return Product.objects.create(
        name='Laptop', sku='LAP001', unit_price=50000,
        quantity=20, low_stock_threshold=5,
        warehouse=warehouse, category=category, supplier=supplier
    )


# --- Category Tests ---
@pytest.mark.django_db
def test_staff_can_list_categories(api_client, staff_user, category):
    api_client.force_authenticate(user=staff_user)
    response = api_client.get('/api/categories/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_can_create_category(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    response = api_client.post('/api/categories/', {'name': 'Furniture'})
    assert response.status_code == 201


@pytest.mark.django_db
def test_staff_cannot_create_category(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    response = api_client.post('/api/categories/', {'name': 'Furniture'})
    assert response.status_code == 403


# --- Supplier Tests ---
@pytest.mark.django_db
def test_admin_can_create_supplier(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    payload = {
        'name': 'New Supplier',
        'email': 'new@supplier.com',
        'phone': '1234567890'
    }
    response = api_client.post('/api/suppliers/', payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_staff_cannot_create_supplier(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)
    payload = {'name': 'New Supplier', 'email': 'new@supplier.com'}
    response = api_client.post('/api/suppliers/', payload)
    assert response.status_code == 403


# --- Product Tests ---
@pytest.mark.django_db
def test_staff_can_list_products(api_client, staff_user, product):
    api_client.force_authenticate(user=staff_user)
    response = api_client.get('/api/products/')
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_manager_can_create_product(api_client, manager_user, warehouse, category, supplier):
    api_client.force_authenticate(user=manager_user)
    payload = {
        'name': 'Monitor', 'sku': 'MON001',
        'unit_price': '15000.00', 'quantity': 10,
        'low_stock_threshold': 3,
        'warehouse': warehouse.id,
        'category': category.id,
        'supplier': supplier.id,
    }
    response = api_client.post('/api/products/', payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_staff_cannot_create_product(api_client, staff_user, warehouse, category, supplier):
    api_client.force_authenticate(user=staff_user)
    payload = {
        'name': 'Monitor', 'sku': 'MON001',
        'unit_price': '15000.00', 'quantity': 10,
        'warehouse': warehouse.id,
        'category': category.id,
        'supplier': supplier.id,
    }
    response = api_client.post('/api/products/', payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_product_low_stock_flag(product):
    product.quantity = 3
    product.save()
    assert product.is_low_stock is True


@pytest.mark.django_db
def test_only_admin_can_delete_product(api_client, staff_user, product):
    api_client.force_authenticate(user=staff_user)
    response = api_client.delete(f'/api/products/{product.id}/')
    assert response.status_code == 403


# --- Stock Transaction Tests ---
@pytest.mark.django_db
def test_stock_in_increases_quantity(api_client, staff_user, product):
    initial_qty = product.quantity
    api_client.force_authenticate(user=staff_user)
    payload = {
        'product': product.id,
        'transaction_type': 'in',
        'quantity': 10,
        'note': 'New stock arrived',
    }
    response = api_client.post('/api/stock-transactions/', payload)
    assert response.status_code == 201
    product.refresh_from_db()
    assert product.quantity == initial_qty + 10


@pytest.mark.django_db
def test_stock_out_decreases_quantity(api_client, staff_user, product):
    initial_qty = product.quantity
    api_client.force_authenticate(user=staff_user)
    payload = {
        'product': product.id,
        'transaction_type': 'out',
        'quantity': 5,
        'note': 'Dispatched to client',
    }
    response = api_client.post('/api/stock-transactions/', payload)
    assert response.status_code == 201
    product.refresh_from_db()
    assert product.quantity == initial_qty - 5


# --- Purchase Order Tests ---
@pytest.mark.django_db
def test_staff_can_create_purchase_order(api_client, staff_user, product, supplier):
    api_client.force_authenticate(user=staff_user)
    payload = {
        'product': product.id,
        'supplier': supplier.id,
        'quantity': 50,
        'note': 'Urgent reorder',
    }
    response = api_client.post('/api/purchase-orders/', payload)
    assert response.status_code == 201
    assert response.data['status'] == 'pending'


@pytest.mark.django_db
def test_manager_can_approve_purchase_order(api_client, manager_user, staff_user, product, supplier):
    api_client.force_authenticate(user=staff_user)
    order_response = api_client.post('/api/purchase-orders/', {
        'product': product.id,
        'supplier': supplier.id,
        'quantity': 50,
    })
    order_id = order_response.data['id']
    api_client.force_authenticate(user=manager_user)
    response = api_client.post(
        f'/api/purchase-orders/{order_id}/action/',
        {'action': 'approve'}
    )
    assert response.status_code == 200
    assert response.data['message'] == 'Order approved and stock updated'


@pytest.mark.django_db
def test_staff_cannot_approve_purchase_order(api_client, staff_user, product, supplier):
    api_client.force_authenticate(user=staff_user)
    order_response = api_client.post('/api/purchase-orders/', {
        'product': product.id,
        'supplier': supplier.id,
        'quantity': 50,
    })
    order_id = order_response.data['id']
    response = api_client.post(
        f'/api/purchase-orders/{order_id}/action/',
        {'action': 'approve'}
    )
    assert response.status_code == 403
