from django.contrib import admin
from .models import Organization, OrganizationSettings

class OrganizationSettingsInline(admin.StackedInline):
    model = OrganizationSettings
    extra = 0

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    inlines = [OrganizationSettingsInline]

@admin.register(OrganizationSettings)
class OrganizationSettingsAdmin(admin.ModelAdmin):
    list_display = ("organization", "default_low_stock_threshold", "updated_at")
