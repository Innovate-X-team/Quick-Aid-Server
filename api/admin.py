from django.contrib import admin
from .models import ConsumerUser, ProviderUser, Task, Otp

# Register your models here.
admin.site.register(ConsumerUser)
admin.site.register(ProviderUser)
admin.site.register(Task)
admin.site.register(Otp)