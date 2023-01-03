from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.feedback.views import CommentViewSet, LikeAPIView, RatingAPIView, FavouriteAPIView

router = DefaultRouter()
router.register('comment', CommentViewSet)
router.register('like', LikeAPIView)
router.register('rating', RatingAPIView)
router.register('favourite', FavouriteAPIView)

urlpatterns = [
    path('', include(router.urls))
]
