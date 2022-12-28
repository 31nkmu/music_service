from rest_framework import serializers

from applications.product.models import Music


class MusicSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    class Meta:
        model = Music
        fields = '__all__'