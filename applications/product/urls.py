from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import MusicViewSet, MusicPostConfirmAPIView

router = DefaultRouter()
router.register('', MusicViewSet)

urlpatterns = [
    path('post_confirm/<int:pk>/', MusicPostConfirmAPIView.as_view()),
    path('', include(router.urls)),
]