from rest_framework import serializers
from applications.product.tasks import send_paid_confirm
from applications.product.models import Music


class MusicSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    def create(self, validated_data):
        music = Music.objects.create(**validated_data)
        request = self.context.get('request')
        user = request.user.email
        send_paid_confirm.delay(user)
        return music

    class Meta:
        model = Music
        fields = '__all__'

