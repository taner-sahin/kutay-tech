from django.urls import path

from . import views


app_name = "cart"

urlpatterns = [

    # Sepet sayfası
    path(
        "",
        views.cart_detail,
        name="cart_detail",
    ),

    # Sepete ürün ekle
    path(
        "add/",
        views.add_to_cart,
        name="add_to_cart",
    ),

    # Ürün adedini artır
    path(
        "increase/<int:item_id>/",
        views.increase_quantity,
        name="increase_quantity",
    ),

    # Ürün adedini azalt
    path(
        "decrease/<int:item_id>/",
        views.decrease_quantity,
        name="decrease_quantity",
    ),

    # Ürünü tamamen sil
    path(
        "remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
]