# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/add/', views.add_stock, name='add_stock'),
    path('stocks/<int:stock_id>/add-to-inventory/', views.add_to_inventory, name='add_to_inventory'),
    path('stocks/edit/<int:stock_id>/', views.edit_stock, name='edit_stock'),
    path('stocks/delete/<int:stock_id>/', views.delete_stock, name='delete_stock'),
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/edit/<int:inventory_id>/', views.edit_inventory, name='edit_inventory'),
    path('inventory/delete/<int:inventory_id>/', views.delete_inventory, name='delete_inventory'),
    path('alerts/', views.alerts_view, name='alerts'),
]
    