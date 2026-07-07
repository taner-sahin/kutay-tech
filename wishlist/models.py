from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Wishlist(models.Model):
    # Hangi kullanıcı favoriye ekledi?
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    # Hangi ürün favoriye eklendi?
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    # Favoriye eklenme tarihi
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Aynı kullanıcı aynı ürünü birden fazla kez favoriye ekleyemesin
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"