from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from applications.feedback.models import Like, Rating, Favourite
from applications.feedback.serializers import RatingSerializer


class LikeMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = Like.objects.get_or_create(music_id=pk, owner=request.user)
        obj.like = not obj.like
        obj.save()
        status_ = 'Liked'
        if not obj.like:
            status_ = 'Unliked'
        return Response({'msg': status_})


class RatingMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(music_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class FavouriteMixin:
    @action(detail=True, methods=['POST'])
    def post(self, request, pk, *args, **kwargs):
        obj, _ = Favourite.objects.get_or_create(music_id=pk, owner=request.user)
        obj.save()
        return Response(status=status.HTTP_201_CREATED)
