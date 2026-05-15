from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_auth import LoginView, LogoutView, ChangePasswordView, MeView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('me/', MeView.as_view(), name='me'),
]