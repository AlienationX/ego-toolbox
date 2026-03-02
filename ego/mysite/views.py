from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _


def login_view(request):
    """登录视图"""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next", "/toolbox/")
                return redirect(next_page)
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


def register_view(request):
    """注册视图"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/toolbox/")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def logout_view(request):
    """登出视图"""
    if request.method == "POST":
        logout(request)
        messages.success(request, _("您已成功登出"))
        return redirect("my_login")
    return redirect("my_login")
