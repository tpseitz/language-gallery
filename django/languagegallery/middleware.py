import time
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject


User = get_user_model()


def _get_user(user_id):
  user = AnonymousUser

  user = User.objects.get(pk=user_id)

  return user


class AuthMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    auth = request.headers.get('authorization')

    if not auth or ' ' not in auth:
      return self.get_response(request)

    auth_type, auth_data = auth.split(' ', 1)
    auth_type = auth_type.lower()
    auth_data = auth_data.strip()

    if auth_type == 'bearer' and not request.user.is_authenticated:
      try:
        token_data = jwt.decode(auth_data, settings.SECRET_KEY,
            require_exp=True, verify_exp=True,
            algorithms=settings.JWT_ALGORITHMS)

        if token_data.get('exp', 0) > time.time(): 
          request.user = SimpleLazyObject(lambda: _get_user(token_data['uid']))
      except jwt.exceptions.ExpiredSignatureError:
        pass

    return self.get_response(request)

