from django.contrib import admin

from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # Admin listesindeki sütunlar
    list_display = (
        "user",
        "product_name",
        "variant",
        "quantity",
        "subtotal",
        "created_at",
    )

    # Sağ tarafta filtreleme alanı
    list_filter = (
        "created_at",
        "variant__is_active",
    )

    # Kullanıcı, ürün, renk ve bedene göre arama
    search_fields = (
        "user__username",
        "variant__product__name",
        "variant__color",
        "variant__size",
    )

    # ForeignKey seçimlerini daha kullanışlı hale getirir
    autocomplete_fields = (
        "user",
        "variant",
    )

    @admin.display(description="Ürün")
    def product_name(self, obj):
        """
        CartItem doğrudan Product'a bağlı olmadığı için
        ürüne variant üzerinden ulaşırız.
        """

        if obj.variant:
            return obj.variant.product.name

        return "Varyant seçilmedi"