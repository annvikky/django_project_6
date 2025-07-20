from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone_number", "avatar", "city"]
        extra_kwargs = {
            "email": {"help_text": "Уникальный Email пользователя"},
            "username": {"help_text": "Имя пользователя (необязательное)"},
            "phone_number": {"help_text": "Номер телефона"},
            "avatar": {"help_text": "Аватар пользователя"},
            "city": {"help_text": "Город проживания"},
            "telegram_chat_id": {"help_text": "Chat ID в Telegram для уведомлений"},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, min_length=6, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "phone_number",
            "avatar",
            "city",
            "telegram_chat_id",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TelegramConnectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["telegram_chat_id"]

    def update(self, instance, validated_data):
        instance.chat_id = validated_data.get(
            "telegram_chat_id", instance.telegram_chat_id
        )
        instance.save()
        return instance
