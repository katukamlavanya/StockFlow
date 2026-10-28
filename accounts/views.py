from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import SignUpForm
from .models import UserProfile
from organizations.models import Organization, OrganizationSettings

@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save()
            organization = Organization.objects.create(name=form.cleaned_data["organization_name"].strip())
            OrganizationSettings.objects.create(organization=organization, default_low_stock_threshold=5)
            UserProfile.objects.create(user=user, organization=organization)
        login(request, user)
        messages.success(request, "Your StockFlow workspace is ready.")
        return redirect("dashboard:home")
    return render(request, "accounts/signup.html", {"form": form})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Welcome back to StockFlow.")
        return redirect(request.GET.get("next") or "dashboard:home")
    return render(request, "accounts/login.html", {"form": form})
