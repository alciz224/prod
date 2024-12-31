from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from datetime import datetime

class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                settings.JWT_AUTH_COOKIE,
                response.data['access'],
                expires=datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.JWT_AUTH_COOKIE_SECURE,
                httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.JWT_AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                settings.JWT_AUTH_REFRESH_COOKIE,
                response.data['refresh'],
                expires=datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                secure=settings.JWT_AUTH_COOKIE_SECURE,
                httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.JWT_AUTH_COOKIE_SAMESITE
            )
            del response.data['access']
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('access'):
            response.set_cookie(
                settings.JWT_AUTH_COOKIE,
                response.data['access'],
                expires=datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.JWT_AUTH_COOKIE_SECURE,
                httponly=settings.JWT_AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.JWT_AUTH_COOKIE_SAMESITE
            )
            del response.data['access']
        return super().finalize_response(request, response, *args, **kwargs)

class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.JWT_AUTH_COOKIE)
        response.delete_cookie(settings.JWT_AUTH_REFRESH_COOKIE)
        return response

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
