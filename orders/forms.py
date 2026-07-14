from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Checkout sırasında kullanıcıdan teslimat bilgilerini alır.
    """

    class Meta:
        model = Order

        fields = [
            "full_name",
            "phone",
            "address",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Adınız ve soyadınız",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Telefon numaranız",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Teslimat adresiniz",
                    "rows": 4,
                }
            ),
        }

        labels = {
            "full_name": "Ad Soyad",
            "phone": "Telefon",
            "address": "Teslimat Adresi",
        }