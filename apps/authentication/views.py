# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, SignUpForm

# New imports
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.contrib.auth.models import User




# def register_user(request):
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)

#             msg = 'User created - please <a href="/login">login</a>.'
#             success = True

#             # return redirect("/login/")

#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thanks for your email confirmation. Now you can login your account")
        return redirect(reverse("authentication:login"))
    else:
        messages.error(request, "Activation link is invalid!")
    return redirect(reverse("authentication:login"))



def activateEmail(request, user):
    mail_subject = "Activate your user account"
    message =  render_to_string("accounts/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'Protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[user.email])
    email.send()
    # if email.send():
    #     messages.success(request, f'Dear {user.username}, please go to {user.email} inbox and click on \
    #                     received activation link to confirm and complete the registration. Note: Check your spam folder.')
    # else:
    #     messages.error(request, f'Problem sending email to {user.email}. Check if you typed it correctly.')

    
def email_confirm(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render("home/page-404.html")

    activateEmail(request, user)
    return render(request, "accounts/inactive_user.html")



def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None and user.check_password(password):
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                else:
                    return redirect(reverse('authentication:email_confirm', args=[username]))
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})



def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            return redirect(reverse("authentication:email_confirm", args=[user.username]))
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form})