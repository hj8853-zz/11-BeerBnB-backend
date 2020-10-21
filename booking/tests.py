import json
import jwt

from django.test import (
    TestCase,
    Client,
)

from my_settings import ALGORITHM
from room.models import Room
from user.utils import login_required
from user.models import (
    User,
    LoginPlatform,
    Host
)
from .models import (
    Booking,
    BookingStatus,
    PaymentMethod
)


client = Client()

class BookingViewTest(TestCase):
    def setUp(self):
        LoginPlatform.objects.create(
            name = 'google'
        )
        user = User.objects.create(
            email = 'jiwonko@gmail.com',
            password = '1q2w3e4r!',
            first_name = 'jiwon',
            last_name = 'ko',
            birth_date = '1997-02-20',
            is_host = True,
            platform = LoginPlatform.objects.get(name = 'google'),
        )
        host = Host.objects.create(
            user = user,
            is_super_host = True
        )
        room = Room.objects.create(
            id            = 2,
            title         = 'stay_AHHA_01호',
            address       = 'Aewol-eup, Jeju-si, 제주도, 한국',
            max_personnal = '최대 인원 4명',
            bed_room      = '침실 1개',
            bed           = '침대 1개',
            bath_room     = '욕실 1개',
            price         = 78000,
            latitude      = 33.18481000,
            longitude     = 126.37482000,
            description   = "제주도에 놀러오세여여어어여어여여ㅓㅇ아야아이야이야이",
        )
        status = BookingStatus.objects.create(
            status = '예약 대기'
        )
        payment_method = PaymentMethod.objects.create(
            name = '신용 카드'
        )
        booking = Booking.objects.create(
            check_in = '2020-12-01',
            check_out = '2020-12-02',
            price = 78000,
            cleaning_expense = 5600,
            service_tax = 3200,
            accomodation_tax = 4800,
            adult = 4,
            children = 1,
            infants = 0,
            user = user,
            room = room,
            status = status,
            payment_method = payment_method
        )
        with open('secrets.json', 'r') as f:
            secret_key = json.load(f)
        self.token = jwt.encode({'email' : User.objects.get(email = 'jiwonko@gmail.com').email}, secret_key['SECRET_KEY'], algorithm = ALGORITHM).decode('utf-8')

    def tearDown(self):
        User.objects.all().delete()
        LoginPlatform.objects.all().delete()
        Room.objects.all().delete()
        Booking.objects.all().delete()
        BookingStatus.objects.all().delete()
        PaymentMethod.objects.all().delete()

    def test_booking_post_success(self):
        data = {
            "user"          : "request.user",
            "room_id"       : 2,
            "room"          : 2,
            "price"         : 87000,
            "check_in"      : "2020-12-06",
            "check_out"     : "2020-12-08",
            "adult"         : 4,
            "children"      : 0,
            "infants"       : 0,
            "payment_method": "신용 카드",
            "total_price"   : "127800"
        }
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/booking', json.dumps(data), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{'message' : 'SUCCESS'})

    def test_booking_post_not_found_room(self):
        data = {
            "user"          : "request.user",
            "room_id"       : 3,
            "room"          : 2,
            "price"         : 87000,
            "check_in"      : "2020-12-06",
            "check_out"     : "2020-12-08",
            "adult"         : 4,
            "children"      : 0,
            "infants"       : 0,
            "payment_method": "신용 카드",
            "total_price"   : "127800"
        }
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/booking', json.dumps(data), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(),{'message' : 'DOES_NOT_EXIST_ROOM'})

    def test_booking_post_does_not_exist_payment_method_fail(self):
        data = {
            "user"          : "request.user",
            "room_id"       : 2,
            "room"          : 2,
            "price"         : 87000,
            "check_in"      : "2020-12-06",
            "check_out"     : "2020-12-08",
            "adult"         : 4,
            "children"      : 0,
            "infants"       : 0,
            "payment_method": "체크 카드",
            "total_price"   : "127800"
        }
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/booking', json.dumps(data), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'DOES_NOT_EXIST_PAYMENT_METHOD'})

    def test_booking_post_key_error_fail(self):
        data = {
            "user"          : "request.user",
            "room_id"       : 2,
            "room"          : 2,
            "price"         : 87000,
            "check_in"      : "2020-12-06",
            "check_out"     : "2020-12-08",
            "adult"         : 4,
            "childrenssss"  : 0,
            "infants"       : 0,
            "payment_method": "신용 카드",
            "total_price"   : "127800"
        }
        headers  = {'HTTP_Authorization' : self.token}
        response = client.post('/booking', json.dumps(data), **headers, content_type = 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{'message' : 'INVALID_KEY'})