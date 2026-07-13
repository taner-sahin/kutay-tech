from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class CartItem(models.Model):
    # Sepetteki ürünün hangi kullanıcıya ait olduğunu tutar
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # Sepete eklenen ürünü tutar
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # Kullanıcının bu üründen kaç adet eklediğini tutar
    quantity = models.PositiveIntegerField(default=1)

    # Ürünün sepete eklendiği tarihi otomatik kaydeder
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Aynı kullanıcı aynı ürünü ayrı ayrı satırlarda tutmasın
        # Bunun yerine quantity artırılacak
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_cart_item"
            )
        ]

        # Son eklenen ürünler önce gösterilsin
        ordering = ["-created_at"]

    @property
    def subtotal(self):
        # Ürün fiyatı × ürün adedi
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} - "
            f"{self.quantity} adet"
        )