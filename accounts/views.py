from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Kayıt başarılı. Şimdi giriş yapabilirsiniz.")
            return redirect("accounts:login")
        else:
            messages.error(request, "Kayıt başarısız. Bilgileri kontrol edin.")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Başarıyla giriş yaptınız."
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Kullanıcı adı veya şifre hatalı."
            )

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect("home")