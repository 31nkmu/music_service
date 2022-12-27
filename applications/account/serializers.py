from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.account import tasks

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=128, min_length=6, write_only=True)
    password_repeat = serializers.CharField(max_length=128, min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def validate_card_number(self, card_number):
        if not card_number.startswith('4169'):
            raise serializers.ValidationError("Карта виза должна начинаться на '4169'")
        return card_number

    def validate_card_balance(self, card_balance):
        if card_balance < 5000:
            raise serializers.ValidationError('Баланс вашей карты должен быть больше 5000')
        return card_balance

    def create(self, validated_data):

        user = User.objects.create_user(
            password=validated_data['password'],
            email=validated_data['email'],
            card_number=validated_data['card_number'],
            card_balance=validated_data['card_balance'],
            gender=validated_data['gender'],
            is_subscribed=validated_data['is_subscribed'],

        )
        email = user.email
        code = user.activation_code
        tasks.send_user_activation_link.delay(email=email, activation_code=code)
        return user
