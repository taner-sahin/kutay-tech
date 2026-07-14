from django.db import models
from django.contrib.auth.models import User

from products.models import ProductVariant


class CartItem(models.Model):
    """
    Kullanıcının sepetindeki seçilmiş ürün varyantını tutar.

    Örnek:
    Kullanıcı: tanersahin
    Varyant: KUTAY Core Tişört / White / L
    Adet: 2
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "variant"],
                name="unique_user_variant_cart_item",
            )
        ]

        ordering = ["-created_at"]

    @property
    def product(self):
        return self.variant.product

    @property
    def subtotal(self):
        return self.variant.product.price * self.quantity

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.variant.product.name} - "
            f"{self.variant.color or 'Renk yok'} / "
            f"{self.variant.size or 'Seçenek yok'} - "
            f"{self.quantity} adet"
        )