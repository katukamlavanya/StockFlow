from django.db import models
from organizations.models import Organization

class Product(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    low_stock_threshold = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank to use the organization default.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["organization", "sku"], name="unique_sku_per_organization")
        ]

    def effective_low_stock_threshold(self):
        if self.low_stock_threshold is not None:
            return self.low_stock_threshold
        try:
            return self.organization.settings.default_low_stock_threshold
        except Organization.settings.RelatedObjectDoesNotExist:
            return 5

    @property
    def is_low_stock(self):
        return self.quantity <= self.effective_low_stock_threshold()

    def __str__(self):
        return f"{self.name} ({self.sku})"
