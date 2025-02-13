from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app_users.views import RegisterApiView, VerifyEmailApiView, LoginApiView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='register'),
    path('verify/email/', VerifyEmailApiView.as_view(), name='verify_email'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
