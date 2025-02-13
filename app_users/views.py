from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from .serializers import RegisterSerializers # &
from app_users.utils import generate_verification_code, send_verification_email
from app_users.models import ProfileModel


class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = generate_verification_code()

            profile, created = ProfileModel.objects.get_or_create(user=user)
            profile.verification_code = code
            profile.save()

            send_verification_email(user.email, code)
            return Response({"message": "Tasdiqlash kodi yuborildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        user = get_object_or_404(User, email=email)
        profile = user.profile
        if profile.verification_code == code:
            user.is_active = True
            user.save()
            return Response({"message": "Email tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response({"error": "Noto‘g‘ri kod"}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['email'] = self.user.email
        return data


class LoginApiView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

