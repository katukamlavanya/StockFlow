from django import forms
from .models import OrganizationSettings

class OrganizationSettingsForm(forms.ModelForm):
    class Meta:
        model = OrganizationSettings
        fields = ["default_low_stock_threshold"]
        widgets = {
            "default_low_stock_threshold": forms.NumberInput(attrs={"min": 0, "class": "form-control"}),
        }
