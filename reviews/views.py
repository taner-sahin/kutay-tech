from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST


from products.models import Product
from .forms import ReviewForm
from .models import Review


@login_required
@require_POST
def add_review(request, product_id):
    """
    Giriş yapan kullanıcının ürüne yorum eklemesini sağlar.
    """

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    if Review.objects.filter(
        user=request.user,
        product=product,
    ).exists():
        messages.warning(
            request,
            "Bu ürüne daha önce yorum yaptınız.",
        )
        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)

        review.user = request.user
        review.product = product
        review.save()

        messages.success(
            request,
            "Yorumunuz başarıyla eklendi.",
        )
    else:
        messages.warning(
            request,
            "Lütfen puan ve yorum alanlarını doğru doldurun.",
        )

    return redirect(
        "products:product_detail",
        slug=product.slug,
    )
    
@login_required
def update_review(request, review_id):
    """
    Kullanıcının sadece kendi yorumunu düzenlemesini sağlar.
    """

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    if request.method == "POST":
        form = ReviewForm(
            request.POST,
            instance=review,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Yorumunuz güncellendi.",
            )

            return redirect(
                "products:product_detail",
                slug=review.product.slug,
            )
    else:
        form = ReviewForm(instance=review)

    context = {
        "form": form,
        "review": review,
    }

    return render(
        request,
        "reviews/update_review.html",
        context,
    )

@login_required
@require_POST
def delete_review(request, review_id):
    """
    Kullanıcının yalnızca kendi yorumunu silmesini sağlar.
    """

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    product_slug = review.product.slug

    review.delete()

    messages.success(
        request,
        "Yorumunuz silindi.",
    )

    return redirect(
        "products:product_detail",
        slug=product_slug,
    )