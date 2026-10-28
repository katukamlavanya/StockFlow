from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from inventory.models import Product

@login_required
def home(request):
    organization = request.user.profile.organization
    products = Product.objects.filter(organization=organization)
    total_products = products.count()
    total_quantity = products.aggregate(total=Sum("quantity"))["total"] or 0
    all_products = list(products)
    low_stock_products = [p for p in all_products if p.is_low_stock]
    recent_products = products.order_by("-updated_at")[:5]
    return render(request, "dashboard/home.html", {
        "organization": organization,
        "total_products": total_products,
        "total_quantity": total_quantity,
        "low_stock_count": len(low_stock_products),
        "low_stock_products": low_stock_products[:5],
        "recent_products": recent_products,
    })
