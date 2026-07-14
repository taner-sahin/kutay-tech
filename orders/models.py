from django.db import models
from django.contrib.auth.models import User

from products.models import ProductVariant


class Order(models.Model):
    """
    Kullanıcının tamamladığı siparişin ana kaydını tutar.
    """

    STATUS_CHOICES = [
        ("pending", "Hazırlanıyor"),
        ("shipped", "Kargoda"),
        ("delivered", "Teslim Edildi"),
        ("cancelled", "İptal Edildi"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    full_name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=20,
    )

    address = models.TextField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Sipariş #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """
    Siparişin içindeki her bir ürün varyantını tutar.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )

    product_name = models.CharField(
        max_length=200,
    )

    color = models.CharField(
        max_length=100,
        blank=True,
    )

    size = models.CharField(
        max_length=100,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return (
            f"Sipariş #{self.order.id} - "
            f"{self.product_name} - "
            f"{self.quantity} adet"
        )