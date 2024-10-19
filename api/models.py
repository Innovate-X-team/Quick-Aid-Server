from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class ConsumerUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        # Hash the password before saving
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Check if the entered password matches the hashed one
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.username
    
class ProviderUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    service_type = models.CharField(max_length=100)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        # Hash the password before saving
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        # Check if the entered password matches the hashed one
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
    
class Otp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
    

