from django.contrib.auth import get_user_model
from rest_framework import serializers
from django_otp.plugins.otp_email.models import EmailDevice

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.create_otp_device(user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def create_otp_device(self, user):
        device = EmailDevice.objects.create(user=user, email=user.email)
        device.generate_challenge()


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
