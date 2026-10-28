from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .forms import ProductForm
from .models import Product

def _organization(request):
    return request.user.profile.organization

@login_required
def product_list(request):
    organization = _organization(request)
    products = Product.objects.filter(organization=organization)
    query = request.GET.get("q", "").strip()
    filter_by = request.GET.get("stock", "").strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(sku__icontains=query))
    if filter_by == "low":
        products = [p for p in products if p.is_low_stock]
    elif filter_by == "healthy":
        products = [p for p in products if not p.is_low_stock]
    return render(request, "inventory/product_list.html", {
        "products": products, "query": query, "stock_filter": filter_by,
    })

@login_required
@require_http_methods(["GET", "POST"])
def product_create(request):
    organization = _organization(request)
    form = ProductForm(request.POST or None, organization=organization)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.organization = organization
        product.save()
        messages.success(request, f"{product.name} was added to inventory.")
        return redirect("inventory:list")
    return render(request, "inventory/product_form.html", {"form": form, "page_title": "Add product", "button_label": "Add product"})

@login_required
@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    organization = _organization(request)
    product = get_object_or_404(Product, pk=pk, organization=organization)
    form = ProductForm(request.POST or None, instance=product, organization=organization)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{product.name} was updated.")
        return redirect("inventory:list")
    return render(request, "inventory/product_form.html", {"form": form, "page_title": "Edit product", "button_label": "Save changes", "product": product})

@login_required
@require_http_methods(["GET", "POST"])
def product_delete(request, pk):
    organization = _organization(request)
    product = get_object_or_404(Product, pk=pk, organization=organization)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("inventory:list")
    return render(request, "inventory/product_confirm_delete.html", {"product": product})
