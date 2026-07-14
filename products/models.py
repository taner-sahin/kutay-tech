from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
    
    
class ProductVariant(models.Model):
    # Bu varyantın hangi ürüne ait olduğunu belirler
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    # Ürünün renk seçeneği
    color = models.CharField(
        max_length=50,
        blank=True
    )

    # Ürünün beden, boyut veya kapasite seçeneği
    size = models.CharField(
        max_length=50,
        blank=True
    )

    # Sadece bu varyanta ait stok miktarı
    stock = models.PositiveIntegerField(default=0)

    # Varyant satışa açık mı?
    is_active = models.BooleanField(default=True)

    class Meta:
        # Aynı üründe aynı renk ve beden ikinci kez oluşturulamasın
        constraints = [
            models.UniqueConstraint(
                fields=["product", "color", "size"],
                name="unique_product_color_size"
            )
        ]

        ordering = ["product", "color", "size"]

    def __str__(self):
        return (
            f"{self.product.name} - "
            f"{self.color or 'Renk yok'} - "
            f"{self.size or 'Seçenek yok'}"
        )