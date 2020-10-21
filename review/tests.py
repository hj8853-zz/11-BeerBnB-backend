import json
import datetime
import bcrypt
import jwt
from unittest import mock

from django.test import TestCase, Client

from booking.models import Booking, PaymentMethod, BookingStatus
from my_settings    import ALGORITHM
from review.models  import Review
from room.models    import Room, Amenity
from user.models    import User, LoginPlatform, Gender, UserProfile

client = Client()

class RoomReviewPostTest(TestCase):
    def setUp(self):
        with open('secrets.json', 'r') as f:
            secret_key = json.load(f)
        LoginPlatform(
            name = "airbnb"
        ).save()
        User(
            id         = 1,
            email      = 'test1@test.com',
            password   = bcrypt.hashpw("qweasd123!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            first_name = 'jiwon',
            last_name  = 'ko',
            birth_date = datetime.datetime.strptime("1997-2-20", "%Y-%m-%d"),
            is_host    = False,
            platform   = LoginPlatform.objects.get(name = "airbnb")
        ).save()
        Amenity(
            name = 'amenity'
        ).save()
        Room(
            id            = 1,
            title         = 'Room title',
            address       = 'Room 주소',
            max_personnal = '10',
            bed_room      = '침실',
            bed           = '퀸 사이즈',
            bath_room     = '욕실 한 개',
            price         = 100000,
            latitude      = 30,
            longitude     = 50,
            description   = 'room 설명'
        ).save()
        BookingStatus(
            status = '예약완료'
        ).save()
        PaymentMethod(
            name = '체크카드'
        ).save()
        Booking(
            id               = 1,
            check_in         = datetime.datetime.strptime("2020-08-10", "%Y-%m-%d"),
            check_out        = datetime.datetime.strptime("2020-08-12", "%Y-%m-%d"),
            price            = 100000,
            cleaning_expense = 10000,
            service_tax      = 3000,
            accomodation_tax = 3000,
            adult            = 3,
            children         = 1,
            infants          = 0,
            user             = User.objects.get(email = 'test1@test.com'),
            room             = Room.objects.get(title = 'Room title'),
            status           = BookingStatus.objects.get(status = '예약완료'),
            payment_method   = PaymentMethod.objects.get(name = '체크카드'),
            created_at       = datetime.datetime.strptime("2020-08-09", "%Y-%m-%d")
        ).save()
        Review(
            booking             = Booking.objects.get(id = 1),
            content             = '리뷰 내용',
            cleanliness_score   = 4.0,
            communication_score = 5.0,
            check_in_score      = 3.0,
            accuracy_score      = 2.5,
            location_score      = 3.5,
            satisfaction_score  = 4.0,
            created_at = datetime.datetime.strptime("2020-09-01", "%Y-%m-%d")
        ).save()
        self.token = jwt.encode({'email' : User.objects.get(email = 'test1@test.com').email}, secret_key['SECRET_KEY'], algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        LoginPlatform.objects.all().delete()
        User.objects.all().delete()
        Amenity.objects.all().delete()
        Room.objects.all().delete()
        Review.objects.all().delete()
        PaymentMethod.objects.all().delete()
        BookingStatus.objects.all().delete()
        Booking.objects.all().delete()
        Review.objects.all().delete()

    def test_review_key_error(self):
        header = {"HTTP_Authorization" : self.token}
        test_review_data = {
            "book"               : 1,
            "content"            : "리뷰 내용",
            "cleanliness_score"  : 4.0,
            "communication_score": 5.0,
            "check_in_score"     : 3.0,
            "accuracy_score"     : 2.5,
            "location_score"     : 3.5,
            "satisfaction_score" : 4.0
        }
        response = client.post('/review', json.dumps(test_review_data), **header, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    def test_review_post_success(self):
        header = {'HTTP_Authorization': self.token}
        test_review_data = {
            "room_id"               : 1,
            "content"               : "리뷰 내용",
            "cleanliness_score"     : 4.0,
            "communication_score"   : 5.0,
            "check_in_score"        : 3.0,
            "accuracy_score"        : 2.5,
            "location_score"        : 3.5,
            "satisfaction_score"    : 4.0
        }
        response = client.post('/review', json.dumps(test_review_data), **header, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})