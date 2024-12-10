from django.shortcuts import render
from django.http import HttpResponse
from production.models import Reaction
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):
    reactions=Reaction.objects.first()
    print(type(reactions.content_type))
    if request.htmx:
        return HttpResponse('Htmx Request')

    return render(request, 'base.html')



class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop('refresh', None)  # Remove refresh token from JSON response
        if refresh:
            # Set HttpOnly cookie for the refresh token
            response.set_cookie(
                'refresh_token',
                refresh,
                httponly=True,
                secure=True,  # Use HTTPS in production
                samesite='Strict',
            )
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully."})
        response.delete_cookie('refresh_token')
        return response
