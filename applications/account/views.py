from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging

from applications.account.serializers import RegisterSerializer, ForgotPasswordSerializer, \
    ForgotPasswordConfirmSerializer, ChangePasswordSerializer

User = get_user_model()
logger = logging.getLogger('django_logger')


class RegisterApiView(CreateAPIView):
    logger.info('registepr')
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationApiView(ListAPIView):
    logger.info('activation')
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'ваш аккаунт успешно активирован'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'неправильный код активации'})


class ForgotPasswordApiView(CreateAPIView):
    logger.info('forgot_password')
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer


class ForgotPasswordConfirmApiView(CreateAPIView):
    logger.info('forgot_password_confirm')
    queryset = User.objects.all()
    serializer_class = ForgotPasswordConfirmSerializer


class ChangePasswordApiView(CreateAPIView):
    logger.info('change_password')
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
