from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from cart.models import CartItem
from .forms import OrderForm
from .models import OrderItem


@login_required
def checkout(request):
    """
    Kullanıcının sepetini siparişe dönüştürür.
    """

    cart_items = (
        CartItem.objects
        .filter(user=request.user)
        .select_related("variant__product")
    )

    if not cart_items.exists():
        messages.warning(request, "Sepetiniz boş.")
        return redirect("cart:cart_detail")

    cart_total = sum(item.subtotal for item in cart_items)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)

                    order.user = request.user
                    order.total_price = cart_total
                    order.save()

                    for cart_item in cart_items:
                        variant = cart_item.variant

                        if cart_item.quantity > variant.stock:
                            raise ValueError(
                                f"{variant.product.name} için yeterli stok yok."
                            )

                        OrderItem.objects.create(
                            order=order,
                            variant=variant,
                            product_name=variant.product.name,
                            color=variant.color or "",
                            size=variant.size or "",
                            price=variant.product.price,
                            quantity=cart_item.quantity,
                        )

                        variant.stock -= cart_item.quantity
                        variant.save(update_fields=["stock"])

                    cart_items.delete()

            except ValueError as error:
                messages.warning(request, str(error))
                return redirect("cart:cart_detail")

            messages.success(request, "Siparişiniz başarıyla oluşturuldu.")

            return redirect("orders:success")

    else:
        form = OrderForm()

    context = {
        "form": form,
        "cart_items": cart_items,
        "cart_total": cart_total,
    }

    return render(request, "orders/checkout.html", context)

@login_required
def success(request):
    """
    Sipariş başarıyla tamamlandıktan sonra
    kullanıcıya başarı sayfasını gösterir.
    """

    return render(request, "orders/success.html")