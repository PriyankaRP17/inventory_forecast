from django.urls import path

from . import views

urlpatterns = [
    # Warehouse
    path('warehouses/', views.WarehouseListCreateView.as_view(), name='warehouse-list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse-detail'),
    # Category
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    # Supplier
    path('suppliers/', views.SupplierListCreateView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    # Product
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]
