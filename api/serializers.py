from .models import ConsumerUser, ProviderUser, Otp
from rest_framework import serializers

class ConsumerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerUser
        fields = "__all__"

class ProviderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderUser
        fields = "__all__"

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"