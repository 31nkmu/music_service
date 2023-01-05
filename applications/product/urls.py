from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page
from applications.product.views import MusicViewSet, MusicPostConfirmAPIView, AlbumViewSet, HistoryAPIView, BestAPIView

router = DefaultRouter()
router.register('album', AlbumViewSet)
router.register('', MusicViewSet)

urlpatterns = [
    path('post_confirm/<int:pk>/', MusicPostConfirmAPIView.as_view(), name='post-confirm'),
    path('history/', cache_page(300)(HistoryAPIView.as_view()), name='history-list'),
    path('best/', BestAPIView.as_view(), name='best-list'),
    path('', include(router.urls)),
]