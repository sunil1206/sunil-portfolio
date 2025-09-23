import requests
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Sum
from .models import Product, InventoryItem


def dashboard(request):
    """
    Displays the main dashboard with summary statistics and urgent alerts.
    """
    today = date.today()
    tomorrow = today + timedelta(days=1)
    next_7_days = today + timedelta(days=7)

    expiring_tomorrow = InventoryItem.objects.filter(expiry_date=tomorrow)
    expiring_soon = InventoryItem.objects.filter(expiry_date__gt=tomorrow, expiry_date__lte=next_7_days)
    total_items = InventoryItem.objects.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

    context = {
        'expiring_tomorrow_count': expiring_tomorrow.count(),
        'expiring_soon_count': expiring_soon.count(),
        'total_items': total_items,
        'urgent_alerts': expiring_tomorrow.select_related('product'),
    }
    return render(request, 'inventory/dashboard.html', context)


def alert_monitor(request):
    """
    Displays a focused view of all items that need attention.
    """
    today = date.today()
    tomorrow = today + timedelta(days=1)
    next_7_days = today + timedelta(days=7)

    context = {
        'expired_items': InventoryItem.objects.filter(expiry_date__lt=today).select_related('product'),
        'expiring_tomorrow': InventoryItem.objects.filter(expiry_date=tomorrow).select_related('product'),
        'expiring_soon': InventoryItem.objects.filter(expiry_date__gt=tomorrow,
                                                      expiry_date__lte=next_7_days).select_related('product'),
    }
    return render(request, 'inventory/alert_monitor.html', context)


def inventory_list(request):
    """
    Shows a complete, sortable list of all items in the inventory.
    """
    all_items = InventoryItem.objects.all().select_related('product')
    context = {
        'inventory_items': all_items,
    }
    return render(request, 'inventory/inventory_list.html', context)


def scan_item_view(request):
    """
    Handles both displaying the scan form (GET) and processing
    the new inventory item submission (POST).
    """
    if request.method == 'POST':
        try:
            barcode = request.POST.get('barcode')
            # Ensure product exists before creating an inventory item
            product = get_object_or_404(Product, barcode=barcode)

            InventoryItem.objects.create(
                product=product,
                category=request.POST.get('category', 'Uncategorized'),
                rack_zone=request.POST.get('rack_zone', 'N/A'),
                quantity=int(request.POST.get('quantity', 1)),
                expiry_date=request.POST.get('expiry_date')
            )
            return redirect('dashboard')
        except (ValueError, TypeError):
            # A simple fallback in case of bad form data
            return redirect('scan_item')

    return render(request, 'inventory/scan_item.html')


@require_GET
def check_barcode_api(request):
    """
    API endpoint for the frontend to check a barcode. If the product
    is not in the local DB, it fetches it from the French Open Food Facts API.
    """
    barcode = request.GET.get('barcode', '').strip()
    if not barcode:
        return JsonResponse({'error': 'Barcode is required.'}, status=400)

    try:
        product = Product.objects.get(barcode=barcode)
        return JsonResponse({
            'status': 'found_in_db',
            'barcode': product.barcode,
            'name': product.name,
            'brand': product.brand or '',
            'imageUrl': product.image_url or ''
        })
    except Product.DoesNotExist:
        try:
            # Using the French-specific API for better local results
            api_url = f"https://fr.openfoodfacts.org/api/v0/product/{barcode}.json"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
            data = response.json()

            if data.get('status') == 1:
                p_data = data.get('product', {})
                product = Product.objects.create(
                    barcode=barcode,
                    name=p_data.get('product_name', f"Product: {barcode}"),
                    brand=p_data.get('brands', ''),
                    image_url=p_data.get('image_url', '')
                )
                return JsonResponse({
                    'status': 'fetched_from_api',
                    'barcode': product.barcode,
                    'name': product.name,
                    'brand': product.brand or '',
                    'imageUrl': product.image_url or ''
                })
            else:
                return JsonResponse({'error': 'Product not found in Open Food Facts.'}, status=404)
        except requests.RequestException as e:
            return JsonResponse({'error': f'API connection error: {e}'}, status=503)


@require_POST
def delete_inventory_item(request, item_id):
    """
    Deletes an inventory item from the database.
    """
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    # Redirect back to the page the user was on, defaulting to dashboard
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

