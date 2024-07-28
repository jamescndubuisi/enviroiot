from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms


# Create your views here.


@login_required
def homepage(request):
    title = "Enviroiot"
    return render(request, "webiot/index.html", {"title": title})


def login_page(request):
    title = "Login"
    message = ""
    purpose = "Login"
    form = forms.LoginForm
    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user=user)
                return redirect("home")
            else:
                messages.error(request, 'username or password not correct')
                return redirect('log_in')
        else:
            print("Terrible form")
            return render(
                request, "registration/login.html", {"form": form, "message": message}
            )
    return render(
        request,
        "registration/login.html",
        {"form": form, "message": message, "title": title, "purpose": purpose},
    )


def sign_up(request):
    title = "Register"
    context = {"title": title}
    form = forms.CreateUser(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'registration/register.html')
    context['form'] = form
    return render(request, 'registration/register.html', context)
