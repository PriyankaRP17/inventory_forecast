from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsAdmin, IsManager, IsStaff

from .models import Category, Product, Supplier, Warehouse
from .serializers import (CategorySerializer, ProductSerializer,
                          SupplierSerializer, WarehouseSerializer)


class WarehouseListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsStaff()]

    def get(self, request):
        warehouses = Warehouse.objects.all()
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WarehouseDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdmin()]
        return [IsStaff()]

    def get_object(self, pk):
        try:
            return Warehouse.objects.get(pk=pk)
        except Warehouse.DoesNotExist:
            return None

    def get(self, request, pk):
        warehouse = self.get_object(pk)
        if not warehouse:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(WarehouseSerializer(warehouse).data)

    def put(self, request, pk):
        warehouse = self.get_object(pk)
        if not warehouse:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = WarehouseSerializer(warehouse, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        warehouse = self.get_object(pk)
        if not warehouse:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        warehouse.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsStaff()]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdmin()]
        return [IsStaff()]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(CategorySerializer(category).data)

    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplierListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsStaff()]

    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdmin()]
        return [IsStaff()]

    def get_object(self, pk):
        try:
            return Supplier.objects.get(pk=pk)
        except Supplier.DoesNotExist:
            return None

    def get(self, request, pk):
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(SupplierSerializer(supplier).data)

    def put(self, request, pk):
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        supplier = self.get_object(pk)
        if not supplier:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsManager()]
        return [IsStaff()]

    def get(self, request):
        products = Product.objects.select_related(
            'category', 'supplier', 'warehouse'
        ).all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdmin()]
        if self.request.method == 'PUT':
            return [IsManager()]
        return [IsStaff()]

    def get_object(self, pk):
        try:
            return Product.objects.select_related(
                'category', 'supplier', 'warehouse'
            ).get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(ProductSerializer(product).data)

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
