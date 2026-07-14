from django.contrib import admin
from .models import Category, Product,  ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "is_featured",
        "created_at",
    )
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "color",
        "size",
        "stock",
        "is_active",
    )

    list_filter = (
        "is_active",
        "color",
        "size",
    )

    search_fields = (
        "product__name",
        "color",
        "size",
    )