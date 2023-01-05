import logging

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.feedback.mixins import LikeMixin, RatingMixin, FavouriteMixin
from applications.feedback.models import Comment, Like, Rating, Favourite
from applications.feedback.permissions import IsCommentFavouriteOwner
from applications.feedback.serializers import CommentSerializer, LikeSerializer, RatingSerializer, FavouriteSerializer

logger = logging.getLogger('django_logger')


class CommentViewSet(ModelViewSet):
    logger.info('comment')
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentFavouriteOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeAPIView(mixins.ListModelMixin, LikeMixin, GenericViewSet):
    logger.info('like')
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class RatingAPIView(mixins.ListModelMixin, mixins.DestroyModelMixin, RatingMixin, GenericViewSet):
    logger.info('rating')
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class FavouriteAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, FavouriteMixin,
                       GenericViewSet):
    logger.info('favourite')
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [IsCommentFavouriteOwner]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset
