# core/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that retrieves the access token from cookies.
    """
    def authenticate(self, request):
        access_token = request.COOKIES.get('access')
        if access_token:
            try:
                return self.get_user_and_token(access_token)
            except Exception:
                return None
        return None
