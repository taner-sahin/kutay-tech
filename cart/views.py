from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product
from .models import CartItem


@login_required
def cart_detail(request):
    """
    Giriş yapan kullanıcının sepetindeki ürünleri gösterir.
    """

    cart_items = CartItem.objects.filter(
        user=request.user
    ).select_related("product")

    # Sepetteki bütün ürünlerin ara toplamlarını toplar
    cart_total = sum(item.subtotal for item in cart_items)

    context = {
        "cart_items": cart_items,
        "cart_total": cart_total,
    }

    return render(request, "cart/cart_detail.html", context)


@login_required
def add_to_cart(request, product_id):
    """
    Ürünü sepete ekler.

    Ürün sepette yoksa yeni CartItem oluşturur.
    Ürün zaten sepetteyse quantity değerini 1 artırır.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    # Sepette ürün varsa getir, yoksa oluştur
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1},
    )

    if created:
        messages.success(request, "Ürün sepete eklendi.")

    else:
        # Mevcut adet ürün stokundan küçükse artır
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])

            messages.success(
                request,
                "Ürünün sepetteki adedi artırıldı.",
            )
        else:
            messages.warning(
                request,
                "Stok miktarından daha fazla ürün ekleyemezsin.",
            )

    return redirect("cart:cart_detail")


@login_required
def increase_quantity(request, item_id):
    """
    Sepetteki ürün adedini 1 artırır.
    """

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user,
    )

    if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

        messages.success(request, "Ürün adedi artırıldı.")
    else:
        messages.warning(
            request,
            "Stok miktarından daha fazla ürün ekleyemezsin.",
        )

    return redirect("cart:cart_detail")


@login_required
def decrease_quantity(request, item_id):
    """
    Sepetteki ürün adedini 1 azaltır.

    Adet 1 ise ürün sepetten tamamen çıkarılır.
    """

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user,
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save(update_fields=["quantity"])

        messages.success(request, "Ürün adedi azaltıldı.")
    else:
        cart_item.delete()

        messages.success(request, "Ürün sepetten çıkarıldı.")

    return redirect("cart:cart_detail")


@login_required
def remove_from_cart(request, item_id):
    """
    Ürünü miktarına bakmadan sepetten tamamen siler.
    """

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user,
    )

    cart_item.delete()

    messages.success(request, "Ürün sepetten çıkarıldı.")

    return redirect("cart:cart_detail")