import jwt
import json

from django.http import JsonResponse

from .models     import User
from my_settings import ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        with open('secrets.json', 'r') as f:
            secret_key = json.load(f)
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, secret_key['SECRET_KEY'], algorithm = ALGORITHM)
            request.user = User.objects.get(email = payload['email'])
            return func(self, request, *args, **kwargs)
        except User.DoesNotExist:
                JsonResponse({"message" : 'INVALID_USER'}, status = 401)
        except jwt.DecodeError:
            return JsonResponse({"message" : 'INVALID_TOKEN'}, status = 401)
    return wrapper