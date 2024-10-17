from django.urls import include, path
from rest_framework import routers
from api import views


urlpatterns = [
    path('login/', views.login),
    path('create_user/', views.create_user),
    path('verify_email/', views.verify_email),
]
