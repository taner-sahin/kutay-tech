from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]