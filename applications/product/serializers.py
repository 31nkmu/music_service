from django.db.models import Avg
from rest_framework import serializers
from applications.product.tasks import send_paid_confirm
from applications.product.models import Music, Album


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    class Meta:
        model = Album
        fields = '__all__'

    @staticmethod
    def validate_title(title):
        if Album.objects.filter(title=title.lower()).exists():
            raise serializers.ValidationError({'msg': 'такой альбом уже существует'})
        return title


class MusicSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    def create(self, validated_data):
        music = Music.objects.create(**validated_data)
        request = self.context.get('request')
        user = request.user.email
        send_paid_confirm.delay(user)
        return music

    def validate(self, attrs):
        album_singer = attrs['album'].singer
        music_singer = attrs['singer']
        if not album_singer == music_singer:
            raise serializers.ValidationError({'msg': 'исполнитель альбома и песни не совпадают'})
        return attrs

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['likes'] = instance.likes.filter(like=True).count()
        res['ratings'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return res

    class Meta:
        model = Music
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'