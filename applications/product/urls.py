from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import MusicViewSet, MusicPostConfirmAPIView, AlbumViewSet, HistoryAPIView

router = DefaultRouter()
router.register('album', AlbumViewSet)
router.register('', MusicViewSet)

urlpatterns = [
    path('post_confirm/<int:pk>/', MusicPostConfirmAPIView.as_view()),
    path('history/', HistoryAPIView.as_view()),
    path('', include(router.urls)),
]