from django.urls import include, path
from rest_framework import routers
from api import views


urlpatterns = [
    path('login/', views.login),
    path('create_user/', views.create_user),
    path('send_email_otp/', views.send_email_otp),
    path('verify_email/', views.verify_email),
    path('change_password/', views.change_password),
    path('check_username/', views.check_username),
]
