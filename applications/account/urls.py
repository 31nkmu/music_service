from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from applications.account import views

# router = DefaultRouter()
# router.register('', views.RegisterApiView)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', views.RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationApiView.as_view()),
    path('forgot_password/', views.ForgotPasswordApiView.as_view()),
    path('forgot_password_confirm/', views.ForgotPasswordConfirmApiView.as_view()),
]

# urlpatterns += router.urls
