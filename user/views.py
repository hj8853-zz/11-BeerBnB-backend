import json
import re
import bcrypt
import datetime
import jwt
import requests

from django.views import View
from django.http  import JsonResponse

from .models     import User, LoginPlatform
from my_settings import ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            input_email    = data['email']
            input_first    = data['first_name']
            input_last     = data['last_name']
            input_password = data['password']
            login_platform = data['platform']

            input_birth = datetime.datetime.strptime(f"{data['year']}-{data['month']}-{data['day']}", "%Y-%m-%d")
            today = datetime.datetime.today()

            if input_birth.month < today.month:
                age = today.year - int(input_birth.year)
            elif (input_birth.month == today.month) and (input_birth.day <= today.day):
                age = today.year - input_birth.year
            else:
                age = today.year - input_birth.year -1

            name_format = re.compile('^[a-zA-Z0-9-\.\+!]+$')
            password_format = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
            password_format_first = re.compile(input_first)
            password_format_last = re.compile(input_last)
            email_format = re.compile('^([a-zA-Z0-9-_.]+)@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_.]+$')
            if not(email_format.match(input_email)):
                return JsonResponse({'message' : 'INVALID_EMAIL_FORMAT'}, status = 400)
            if not name_format.match(input_first) or not name_format.match(input_last):
                return JsonResponse({'message' : 'INVALID_NAME_FORMAT'}, status = 400)
            email_id = re.findall(email_format, input_email)
            password_format_email = re.compile(email_id[0])
            if input_password != None :
                if password_format_email.search(input_password):
                    return JsonResponse({'message' : 'PASSWORD_CANNOT_CONTAIN_EMAIL'}, status = 400)
                if password_format_first.search(input_password) or password_format_last.search(input_password):
                    return JsonResponse({'message' : 'PASSWORD_CANNOT_CONTAIN_NAME'}, status = 400)
                if not(password_format.search(input_password)):
                    return JsonResponse({'message' : 'INVALID_PASSWORD_FORMAT'}, status = 400)
                password = (bcrypt.hashpw(input_password.encode('utf-8'), bcrypt.gensalt())).decode('utf-8')
            else:
                password = None
            if User.objects.filter(email = input_email).exists():
                return JsonResponse({'message' : 'ALREADY_REGISTERED'}, status = 400)
            if age < 18:
                return JsonResponse({'message' : 'UNDER_THE_AGE_OF_18'}, status = 400)

            User(
                email      = input_email,
                first_name = input_first,
                last_name  = input_last,
                password   = password,
                birth_date = input_birth,
                is_host    = False,
                platform   = LoginPlatform.objects.get(name = login_platform)
            ).save()
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        return JsonResponse({'message' : 'SUCCESS'}, status = 200)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            with open('secrets.json', 'r') as f:
                secret_key = json.load(f)
            input_email    = data['email']
            input_password = data['password']

            email_format = re.compile('^([a-zA-Z0-9-_.]+)@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_.]+$')
            password_format = re.compile('^[A-Za-z\d\W]{8,}$')
            if input_email == "" or input_email == " ":
                return JsonResponse({'message': 'EMPTY_EMAIL'}, status = 400)
            if not(email_format.match(input_email)):
                return JsonResponse({'message' : 'INVALID_EMAIL_FORMAT'}, status = 400)
            if not(password_format.match(input_password)):
                return JsonResponse({'message' : 'INVALID_PASSWORD_FORMAT'}, status = 400)
            if not (User.objects.filter(email = input_email).exists()):
                return JsonResponse({'message': 'NO_EXISTS_USER'}, status = 400)
            user = User.objects.get(email = input_email)
            saved_password = user.password
            if bcrypt.checkpw(input_password.encode('utf-8'), saved_password.encode('utf-8')):
                access_token = jwt.encode({'email' : user.email}, secret_key['SECRET_KEY'], algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse({'access_token' : access_token}, status = 200)
            return JsonResponse({'message' : 'WRONG_PASSWORD'}, status = 400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class GoogleSignInView(View):
    def post(self, request):
        with open('secrets.json', 'r') as f:
            secret_key = json.load(f)
        access_token = request.headers['authorization']
        response     = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={
                    "Authorization" : f"Bearer {access_token}",
                    "Accept"        : "application/json"
                })
        user_info    = response.json()
        email        = user_info.get('email')

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = user_info['email'])
            access_token = jwt.encode({'email': user.email}, secret_key['SECRET_KEY'], algorithm = ALGORITHM).decode('utf-8')
            return JsonResponse({'access_token' : access_token})
        dic = {
            'email'       : user_info.get('email'),
            'given_name'  : user_info.get('given_name'),
            'family_name' : user_info.get('family_name')
        }
        return JsonResponse({'message'     : 'NON_EXISTENT_GOOGLE_USER',
                             'email'       : dic['email'],
                             'given_name'  : dic['given_name'],
                             'family_name' : dic['family_name']}, status = 400)