from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from .forms import OrganizationSettingsForm
from .models import OrganizationSettings

@login_required
@require_http_methods(["GET", "POST"])
def settings_view(request):
    organization = request.user.profile.organization
    settings_obj, _ = OrganizationSettings.objects.get_or_create(organization=organization)
    form = OrganizationSettingsForm(request.POST or None, instance=settings_obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Organization settings saved.")
        return redirect("organizations:settings")
    return render(request, "organizations/settings.html", {"form": form, "organization": organization})
