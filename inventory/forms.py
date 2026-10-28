from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "description", "quantity", "cost_price", "selling_price", "low_stock_threshold"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Wireless Mouse"}),
            "sku": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. ACC-001"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional product details"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "cost_price": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.01"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.01"}),
            "low_stock_threshold": forms.NumberInput(attrs={"class": "form-control", "min": 0, "placeholder": "Use organization default"}),
        }

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.organization = organization

    def clean_sku(self):
        sku = self.cleaned_data["sku"].strip()
        qs = Product.objects.filter(organization=self.organization, sku__iexact=sku)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This SKU is already used in your organization.")
        return sku
