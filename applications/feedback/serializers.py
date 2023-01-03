from rest_framework import serializers

from applications.feedback.models import Comment, Like, Rating, Favourite


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['music'] = instance.music.title
        return res


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['like', 'music']

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['music'] = instance.music.title
        if instance.like is True:
            res['like'] = 'Liked'
        else:
            res['like'] = 'Unliked'
        return res


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    music = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ['rating', 'music']


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['owner'] = instance.owner.email
        rep['music'] = instance.music.title
        return rep