from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Kullanıcının ürüne puan ve yorum vermesini sağlar.
    """

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {
            "rating": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Ürün hakkındaki yorumunuzu yazın.",
                }
            ),
        }

        labels = {
            "rating": "Puan",
            "comment": "Yorum",
        }