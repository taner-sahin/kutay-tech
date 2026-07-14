from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import ProductVariant
from .models import CartItem


@login_required
def cart_detail(request):
    """
    Giriş yapan kullanıcının sepetini gösterir.
    Varyantla birlikte ana ürün bilgilerini tek sorguda getirir.
    """

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related("variant__product")
    )

    cart_total = sum(item.subtotal for item in cart_items)

    context = {
        "cart_items": cart_items,
        "cart_total": cart_total,
    }

    return render(request, "cart/cart_detail.html", context)


@login_required
@require_POST
def add_to_cart(request):
    """
    Ürün detay formundan gönderilen variant_id değerini alır
    ve seçilen varyantı kullanıcının sepetine ekler.
    """

    variant_id = request.POST.get("variant_id")

    if not variant_id:
        messages.warning(request, "Lütfen bir ürün seçeneği seç.")

        return redirect(
            request.META.get("HTTP_REFERER", "home")
        )

    variant = get_object_or_404(
        ProductVariant.objects.select_related("product"),
        id=variant_id,
        is_active=True,
        product__is_active=True,
    )

    if variant.stock <= 0:
        messages.warning(request, "Seçtiğin ürün seçeneği stokta yok.")

        return redirect(
            request.META.get("HTTP_REFERER", "home")
        )

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        variant=variant,
        defaults={"quantity": 1},
    )

    if created:
        messages.success(
            request,
            "Seçtiğin ürün sepete eklendi.",
        )
    else:
        if cart_item.quantity < variant.stock:
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])

            messages.success(
                request,
                "Ürünün sepetteki adedi artırıldı.",
            )
        else:
            messages.warning(
                request,
                "Bu varyantın stok miktarından daha fazla ekleyemezsin.",
            )

    return redirect("cart:cart_detail")


@login_required
@require_POST
def increase_quantity(request, item_id):
    """
    Sepetteki seçili varyantın adedini bir artırır.
    """

    cart_item = get_object_or_404(
        CartItem.objects.select_related("variant"),
        id=item_id,
        user=request.user,
    )

    if cart_item.quantity < cart_item.variant.stock:
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

        messages.success(request, "Ürün adedi artırıldı.")
    else:
        messages.warning(
            request,
            "Bu varyantın stok miktarından daha fazla ekleyemezsin.",
        )

    return redirect("cart:cart_detail")


@login_required
@require_POST
def decrease_quantity(request, item_id):
    """
    Sepetteki ürün adedini bir azaltır.
    Adet bir ise sepet kaydını tamamen siler.
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
@require_POST
def remove_from_cart(request, item_id):
    """
    Seçilen sepet kaydını tamamen siler.
    """

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        user=request.user,
    )

    cart_item.delete()

    messages.success(request, "Ürün sepetten çıkarıldı.")

    return redirect("cart:cart_detail")