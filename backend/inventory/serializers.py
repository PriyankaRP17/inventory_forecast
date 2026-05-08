from rest_framework import serializers
from .models import Category, Product, PurchaseOrder, StockTransaction, Supplier, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location', 'created_at']
        read_only_fields = ['created_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True
    )
    warehouse_name = serializers.CharField(
        source='warehouse.name', read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'description',
            'category', 'category_name',
            'supplier', 'supplier_name',
            'warehouse', 'warehouse_name',
            'quantity', 'low_stock_threshold',
            'unit_price', 'is_low_stock',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class StockTransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_username = serializers.CharField(
        source='created_by.username', read_only=True
    )

    class Meta:
        model = StockTransaction
        fields = [
            'id', 'product', 'product_name',
            'transaction_type', 'quantity',
            'note', 'created_by', 'created_by_username',
            'created_at',
        ]
        read_only_fields = ['created_by', 'created_at']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    requested_by_username = serializers.CharField(
        source='requested_by.username', read_only=True
    )

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'product', 'product_name',
            'supplier', 'supplier_name',
            'quantity', 'status',
            'requested_by', 'requested_by_username',
            'approved_by', 'note',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['requested_by', 'approved_by', 'status', 'created_at', 'updated_at']
