from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Review(models.Model):
    """
    Kullanıcının bir ürüne verdiği puan ve yorumu tutar.
    """

    RATING_CHOICES = [
        (1, "1 Yıldız"),
        (2, "2 Yıldız"),
        (3, "3 Yıldız"),
        (4, "4 Yıldız"),
        (5, "5 Yıldız"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_review",
            )
        ]

        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.product.name} - "
            f"{self.rating} yıldız"
        )