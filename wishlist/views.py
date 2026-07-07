from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from products.models import Product
from .models import Wishlist


@login_required
def wishlist_detail(request):
    # Sadece giriş yapan kullanıcının favorileri çekilir
    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(request, "wishlist/wishlist_detail.html", {
        "wishlist_items": wishlist_items
    })


@login_required
def add_to_wishlist(request, product_id):
    # URL'den gelen product_id ile ürün bulunur
    product = get_object_or_404(Product, id=product_id)

    # Aynı ürün zaten favorilerde yoksa oluşturulur
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        messages.success(request, "Ürün favorilere eklendi.")
    else:
        messages.info(request, "Bu ürün zaten favorilerinde var.")

    return redirect("wishlist:wishlist_detail")


@login_required
def remove_from_wishlist(request, item_id):
    # Sadece giriş yapan kullanıcının kendi favori kaydı silinir
    wishlist_item = get_object_or_404(
        Wishlist,
        id=item_id,
        user=request.user
    )

    wishlist_item.delete()
    messages.success(request, "Ürün favorilerden çıkarıldı.")

    return redirect("wishlist:wishlist_detail")