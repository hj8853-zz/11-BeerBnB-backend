import datetime
import json
import bcrypt
import jwt
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client

from .models     import User, LoginPlatform
from my_settings import ALGORITHM

client = Client()

class SignupTest(TestCase):
    def setUp(self):
        LoginPlatform(
            name = "airbnb"
        ).save()
        User(
            email      = "test1@test.com",
            first_name = "jiwon",
            last_name  = "ko",
            password   = bcrypt.hashpw("qweasd123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birth_date = datetime.datetime.strptime("1997-2-20", "%Y-%m-%d").date(),
            is_host    = False,
            platform   = LoginPlatform.objects.get(name = "airbnb")
        ).save()

    def tearDown(self):
        LoginPlatform.objects.all().delete()
        User.objects.all().delete()

    def test_invalid_email_format(self):
        test_user_data = {
            "email"      : "test1testcom",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd123!",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_EMAIL_FORMAT'})

    def test_password_contain_email(self):
        test_user_data = {
            "email"      : "test1@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "test123!",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'PASSWORD_CANNOT_CONTAIN_EMAIL'})

    def test_password_contain_name(self):
        test_user_data = {
            "email"      : "test1@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "jiwon123!",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'PASSWORD_CANNOT_CONTAIN_NAME'})

    def test_invalid_password_format(self):
        test_user_data = {
            "email"      : "test1@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD_FORMAT'})

    def test_exists_user(self):
        test_user_data = {
            "email"      : "test1@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd123!",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'ALREADY_REGISTERED'})

    def test_under_age_18(self):
        test_user_data = {
            "email"      : "test2@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd123!",
            "year"       : "2009",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'UNDER_THE_AGE_OF_18'})

    def test_signin_key_error(self):
        test_user_data = {
            "id"         : "test2@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd123!",
            "year"       : "2009",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    def test_signup_success(self):
        test_user_data = {
            "email"      : "test3@test.com",
            "first_name" : "jiwon",
            "last_name"  : "ko",
            "password"   : "qweasd123!",
            "year"       : "1997",
            "month"      : "02",
            "day"        : "20",
            "platform"   : "airbnb"
        }
        response = client.post('/user/signup', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})

class SigninTest(TestCase):
    def setUp(self):
        LoginPlatform(
            name = "airbnb"
        ).save()
        User(
            email      = "test1@test.com",
            first_name = "jiwon",
            last_name  = "ko",
            password   = bcrypt.hashpw("qweasd123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birth_date = datetime.datetime.strptime("1997-2-20", "%Y-%m-%d").date(),
            is_host    = False,
            platform   = LoginPlatform.objects.get(name = "airbnb")
        ).save()

    def tearDown(self):
        LoginPlatform.objects.all().delete()
        User.objects.all().delete()

    def test_empty_email(self):
        test_user_data = {
            "email"      : " ",
            "password"   : "qweasd123!"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'EMPTY_EMAIL'})

    def test_invalid_email_format(self):
        test_user_data = {
            "email"      : "test1test.com",
            "password"   : "qweasd123!"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_EMAIL_FORMAT'})

    def test_invalid_password_format(self):
        test_user_data = {
            "email"    : "test1@test.com",
            "password" : "qwea"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_PASSWORD_FORMAT'})

    def test_exists_user(self):
        test_user_data = {
            "email"    : "test5@test.com",
            "password" : "qweasd123"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'NO_EXISTS_USER'})

    def test_wrong_password(self):
        test_user_data = {
            "email"    : "test1@test.com",
            "password" : "qweasd123123!"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'WRONG_PASSWORD'})

    def test_signin_key_error(self):
        test_user_data = {
            "id"       : "test5@test.com",
            "password" : "qweasd123"
        }
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

    def test_signin_success(self):
        with open('secrets.json', 'r') as f:
            secret_key = json.load(f)
        test_user_data = {
            "email"    : "test1@test.com",
            "password" : "qweasd123!"
        }
        user = User.objects.get(email='test1@test.com')
        access_token = jwt.encode({'email': user.email}, secret_key['SECRET_KEY'], algorithm=ALGORITHM).decode('utf-8')
        response = client.post('/user/signin', json.dumps(test_user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'access_token' : access_token})

class GoogleSigninTest(TestCase):
    def setUp(self):
        LoginPlatform(
            name = "google"
        ).save()
        User(
            email      = "google1@test.com",
            first_name = "jiwon",
            last_name  = "ko",
            password   = bcrypt.hashpw("qweasd123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birth_date = datetime.datetime.strptime("1997-2-20", "%Y-%m-%d").date(),
            is_host    = False,
            platform   = LoginPlatform.objects.get(name = "google")
        ).save()

    def tearDown(self):
        LoginPlatform.objects.all().delete()
        User.objects.all().delete()

    @patch('user.views.requests')
    def test_google_signin_success(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                    "email"       : "google1@test.com",
                    "given_name"  : "jiwon",
                    "family_name" : "ko",
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        header = {'HTTP_Authorization': 'fake_token.1234'}
        response = client.post('/user/google', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'access_token': response.json()['access_token']})

    @patch('user.views.requests')
    def test_non_existent_google_user(self, mocked_requests):
        class MockedResponse:
            def json(self):
                return {
                    "email": "google2@test.com",
                    "given_name": "jiwon",
                    "family_name": "kim",
                }
        mocked_requests.get = MagicMock(return_value=MockedResponse())
        header = {'HTTP_Authorization': 'fake_token.1234'}
        response = client.post('/user/google', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'NON_EXISTENT_GOOGLE_USER', 'email' : 'google2@test.com', 'given_name' : 'jiwon', 'family_name' : 'kim'})


