from rest_framework import serializers

from .models import Category, Product, Supplier, Warehouse


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
