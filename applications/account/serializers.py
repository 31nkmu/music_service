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

    @staticmethod
    def validate_card_number(card_number):
        if not card_number.startswith('4169'):
            raise serializers.ValidationError("Карта виза должна начинаться на '4169'")
        if len(card_number) != 16:
            raise serializers.ValidationError("Количество цифр в карте должно быть 16")
        return card_number

    @staticmethod
    def validate_card_balance(card_balance):
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


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('нет такого зарегистрированного пользователя')
        return email

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.create_activation_code()
        user.save()
        tasks.send_user_forgot_password_code.delay(email=user.email, activation_code=user.activation_code)
        return user


class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, min_length=6, max_length=128)
    password_repeat = serializers.CharField(required=True, write_only=True, min_length=6, max_length=128)

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs['password_repeat']
        if p1 != p2:
            return serializers.ValidationError('Пароли не совпадают')
        return attrs

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('нет такого зарегистрированного пользователя')
        return email

    @staticmethod
    def validate_code(code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('неправильный код подтверждения')
        return code

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.activation_code = ''
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6, write_only=True)
    new_password = serializers.CharField(required=True, min_length=6, write_only=True)
    new_password_repeat = serializers.CharField(required=True, min_length=6, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_repeat']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save()
        return user
