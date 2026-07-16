from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.success, name="success"),
    path(
    "my-orders/",
    views.my_orders,
    name="my_orders",
),
    
    path(
    "my-orders/<int:order_id>/",
    views.order_detail,
    name="order_detail",
),
]