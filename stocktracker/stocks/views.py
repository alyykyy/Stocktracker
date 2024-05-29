# inventory/views.py
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock, Inventory
from .forms import StockForm, InventoryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stocks/stock_list.html', {'stocks': stocks})


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'stocks/add_stock.html', {'form': form})


@login_required
def edit_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()  # Save the form data to update the stock object
            return redirect('stock_list')  # Redirect to the stock list
    else:
        form = StockForm(instance=stock)  # Populate the form with existing stock data
    return render(request, 'stocks/edit_stock.html', {'form': form, 'stock': stock})


@login_required
def delete_stock(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        stock.delete()
        return redirect('stock_list')  # Redirect to the stock list
    return render(request, 'stocks/confirm_delete.html', {'stock': stock})

@login_required
def add_to_inventory(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if quantity <= stock.quantity:
                try:
                    inventory_item = Inventory.objects.get(stock=stock)
                    inventory_item.quantity += quantity
                except Inventory.DoesNotExist:
                    inventory_item = Inventory(stock=stock, quantity=quantity)
                
                stock.quantity -= quantity
                stock.save()
                inventory_item.save()
                return redirect('stock_list')
            else:
                form.add_error('quantity', 'Not enough stock available')
    else:
        form = InventoryForm()
    return render(request, 'stocks/add_to_inventory.html', {'form': form, 'stock': stock})



@login_required
def inventory_list(request):
    inventory_items = Inventory.objects.select_related('stock').all()
    return render(request, 'stocks/inventory_list.html', {'inventory_items': inventory_items})


@login_required
def edit_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('inventory_list')
    else:
        form = InventoryForm(instance=inventory_item)
    return render(request, 'stocks/edit_inventory.html', {'form': form, 'inventory_item': inventory_item})


@login_required
def delete_inventory(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory_item.delete()
        return redirect('inventory_list')
    return render(request, 'stocks/delete_inventory.html', {'inventory_item': inventory_item})


@login_required
def alerts_view(request):
    today = timezone.now().date()
    expired = Stock.objects.filter(expiry_date__lt=today)
    almost_expired = Stock.objects.filter(expiry_date__gte=today, expiry_date__lte=today + timedelta(days=30))
    critically_low = Stock.objects.filter(quantity__lte=10)
    low_stock = Stock.objects.filter(quantity__gt=10, quantity__lte=20)

    context = {
        'expired': expired,
        'almost_expired': almost_expired,
        'critically_low': critically_low,
        'low_stock': low_stock,
    }

    return render(request, 'stocks/alerts.html', context)
