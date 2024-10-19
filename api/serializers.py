from .models import ConsumerUser, ProviderUser, Otp
from rest_framework import serializers

class ConsumerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerUser
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = ConsumerUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProviderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderUser
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = ConsumerUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"