# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, activate, email_confirm
from django.contrib.auth import views as auth_views  #<-- Changed
from django.urls import reverse_lazy

app_name = "authentication"

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_templates/password_recovery.html",
                                                      email_template_name="accounts/password_templates/password_reset_email.html",
                                                      success_url = reverse_lazy("authentication:password_reset_done")),
                                                      name="password_reset"),

    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_templates/password_reset_done.html'), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("authentication:password_reset_complete"),
                                                                                template_name='accounts/password_templates/password_reset_confirm.html'),
                                                                                name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_templates/password_reset_complete.html'), name='password_reset_complete'),

    path('activate/<uidb64>/<token>', activate, name='activate'),

    path('email_confirm/<str:username>/', email_confirm, name='email_confirm'),
]
