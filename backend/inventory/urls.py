from django.urls import path

from . import views

urlpatterns = [
    # Warehouse
    path('warehouses/', views.WarehouseListCreateView.as_view()),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view()),
    # Category
    path('categories/', views.CategoryListCreateView.as_view()),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view()),
    # Supplier
    path('suppliers/', views.SupplierListCreateView.as_view()),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view()),
    # Product
    path('products/', views.ProductListCreateView.as_view()),
    path('products/<int:pk>/', views.ProductDetailView.as_view()),
    # Stock
    path('stock-transactions/', views.StockTransactionListCreateView.as_view()),
    # Purchase Orders
    path('purchase-orders/', views.PurchaseOrderListCreateView.as_view()),
    path('purchase-orders/<int:pk>/action/', views.PurchaseOrderApprovalView.as_view()),
]
