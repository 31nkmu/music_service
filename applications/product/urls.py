from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.product.views import MusicViewSet

router = DefaultRouter()
router.register('', MusicViewSet)

urlpatterns = [
    path('', include(router.urls)),
]