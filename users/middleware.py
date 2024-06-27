import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
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
            raise AuthenticationFailed('Token is expired')
        except jwt.InvalidSignatureError:
            logger.error('Token signature is invalid')
            raise AuthenticationFailed('Token signature is invalid')
        except jwt.DecodeError:
            logger.error('Error decoding token')
            raise AuthenticationFailed('Error decoding token')

        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=payload['id'])
            request.user = user
        except user_model.DoesNotExist:
            logger.error('User not found for token')
            raise AuthenticationFailed('User not found')
