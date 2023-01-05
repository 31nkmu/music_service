from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from applications.product.models import Music, Album
from applications.product.permissions import IsOwner
from applications.product.serializers import MusicSerializer, AlbumSerializer, HistorySerializer

User = get_user_model()


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class MusicViewSet(ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = [IsOwner]
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['singer', 'album']
    search_fields = ['title', 'singer', 'album']
    ordering_fields = ['data_added']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Music.objects.filter(is_paid=True)


class MusicPostConfirmAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        music = get_object_or_404(Music, id=pk)
        owner_money = music.owner.card_balance
        cost = owner_money - 250
        if cost < 0:
            return Response({'msg': 'у вас недостаточно денег на балансе'})
        user = User.objects.get(email=music.owner.email)
        user.card_balance = cost
        music.is_paid = True
        user.save()
        music.save()
        return Response({'msg': 'ваша песня в активном пользование'}, status=status.HTTP_200_OK)


class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HistoryAPIView(ListAPIView):
    queryset = Music.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Music.objects.filter(owner=self.request.user)


class BestAPIView(APIView):

    @staticmethod
    def get(request):
        musics = Music.objects.filter(is_paid=True).order_by('likes')[:5]
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data)