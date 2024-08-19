import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            logger.error('Token is expired')
            return redirect('/login?error=expired')  # Redirect to login with error message
        except jwt.InvalidSignatureError:
            logger.error('Token signature is invalid')
            return redirect('/login?error=invalid_signature')  # Redirect to login with error message
        except jwt.DecodeError:
            logger.error('Error decoding token')
            return redirect('/login?error=decode_error')  # Redirect to login with error message

        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=payload['id'])
            request.user = user
        except user_model.DoesNotExist:
            logger.error('User not found for token')
            return redirect('/login?error=user_not_found')  # Redirect to login with error message
