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
    path('onduty_toggle/', views.onduty_toggle),
    path('is_onduty/', views.is_onduty),
    path('call_service/', views.call_service),
    path('update_location/', views.update_location),
    path('get_assigned_task/', views.get_assigned_task),
    path('accept_task/', views.accept_task),
    path('complete_task/', views.complete_task),
]
