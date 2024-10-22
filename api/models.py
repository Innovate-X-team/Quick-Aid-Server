from django.db import models
# from django.contrib.gis.db import models as gis_models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class ConsumerUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    service_request = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)
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
    district = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255)
    on_duty = models.BooleanField(default=False)
    on_work = models.BooleanField(default=False)
    task_assigned = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True, blank=True)
    device_token = models.CharField(max_length=255, null=True, blank=True)
    current_lat = models.FloatField(null=True, blank=True)
    current_lon = models.FloatField(null=True, blank=True)
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
    

class Task(models.Model):
    consumer = models.ForeignKey(ConsumerUser, on_delete=models.CASCADE)
    provider = models.ForeignKey(ProviderUser, null=True, blank=True, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=255, null=True, blank=True)
    requestActive = models.IntegerField(default=10)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.consumer.username} - {self.task_type}"
    
class Otp(models.Model):
    email = models.EmailField(unique=True)
    otp = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.otp}"
    

