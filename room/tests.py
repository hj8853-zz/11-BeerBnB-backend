from django.test import (
    TestCase,
    Client
)

from .models import (
    Room,
    BuildingType,
    Image,
    Tag,
    RuleUse,
    HealthSafety,
    RefundPolicy,
    Amenity,
    RoomAmenity,
    BedType,
    BedRoom,
    BedTypeRoom
)
from user.models import (
    User,
    Host,
    LoginPlatform
)

client = Client()

class RoomsViewTest(TestCase):
    maxDiff = None
    def setUp(self):
        platform = LoginPlatform.objects.create(
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
            is_super_host = True,
            user = user
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
            host          = host
        )
        useable_amenity = Amenity.objects.create(
            name = '주방',
            room = room
        )
        unuseable_amenity = Amenity.objects.create(
            name = '이용 불가: 일산화탄소 경보기',
            room = room
        )
        image = Image.objects.create(
            image_url = 'www.naver.com, www.google.com',
            room      = room
        )
        RoomAmenity.objects.create(
            room    = room,
            amenity = useable_amenity
        )
        RoomAmenity.objects.create(
            room    = room,
            amenity = unuseable_amenity
        )
        buildingtype = BuildingType.objects.create(
            sub_title = '대중님이 호스팅하는 B&b의 개인실',
            room      = room
        )
        tag = Tag.objects.create(
            title  = "청결 강화, 훌륭한 숙소 위치, 11월 26일 4:00 PM까지 무료 취소 가능",
            detail = "최근 숙박한 게스트 중 90%가 위치에 별점 5점을 준 숙소입니다.,그 후에는 12월 1일 4:00 PM 전에 예약을 취소하면 첫 1박 요금 및 서비스 수수료를 제외한 요금의 50%가 환불됩니다.",
            room   = room
        )
        rule_of_use = RuleUse.objects.create(
            rules_of_use = "체크인 시간: 오후 4:00 이후, 체크아웃 시간: 오후 12:00, 흡연 금지",
            room         = room
        )
        health_and_safety = HealthSafety.objects.create(
            health_and_safety = "에어비앤비 청결 강화 기준을 준수합니다., 에어비앤비의 사회적 거리 두기 및 관련 가이드라인이 적용됩니다.",
            room              = room
        )
        refund_policy = RefundPolicy.objects.create(
            refund_policy = "11월 26일 4:00 PM까지 무료 취소 가능",
            room          = room
        )
        bedroom = BedRoom.objects.create(
            name = "싱글 침대 2개, 슈퍼싱글 2개"
        )
        bedtype = BedType.objects.create(
            name = "1번 침실, 2번 침실",
        )
        bed_type_room = BedTypeRoom.objects.create(
            bedtype = bedtype,
            bedroom = bedroom,
            room    = room
        )

    def tearDown(self):
        LoginPlatform.all().delete()
        User.objects.all().delete()
        Host.objects.all().delete()
        Room.objects.all().delete()
        BuildingType.objects.all().delete()
        Image.objects.all().delete()
        Tag.objects.all().delete()
        RuleUse.objects.all().delete()
        HealthSafety.objects.all().delete()
        RefundPolicy.objects.all().delete()
        Amenity.objects.all().delete()
        RoomAmenity.objects.all().delete()
        BedType.objects.all().delete()
        BedRoom.objects.all().delete()
        BedTypeRoom.objects.all().delete()

    def test_rooms_get_success(self):
        response = client.get('/rooms?refund=s&home_type=guest_room&home_type=private_room&limit=10&offset=0')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
        "rooms_list": [
            {
                "id"           : 2,
                "image_url"    : ['www.naver.com, www.google.com'],
                "address"      : "Aewol-eup, Jeju-si, 제주도, 한국",
                "title"        : "stay_AHHA_01호",
                "max_personnal": "최대 인원 4명",
                "bed_room"     : "침실 1개",
                "bed"          : "침대 1개",
                "bath_room"    : "욕실 1개",
                "amenity"      : ['주방', '이용 불가: 일산화탄소 경보기'],
                "price"        : "78000.00",
                "latitude"     : "33.18481000",
                "longitude"    : "126.37482000",
                "host"         : True
            },
        ],
        'total' : 1
        })

    def test_rooms_get_not_found(self): 
        Room.objects.all().delete()
        response = client.get('/rooms')

        self.assertEqual(response.status_code, 404)

    def test_room_get_success(self): 
        response = client.get('/rooms/2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
        "detail_list": [
            {
                "id"               : 2,
                "address"          : "Aewol-eup, Jeju-si, 제주도, 한국",
                "image_url"        : [ 'www.naver.com, www.google.com' ],
                "title"            : "stay_AHHA_01호",
                "sub_title"        : [ "대중님이 호스팅하는 B&b의 개인실" ],
                "max_personnal"    : "최대 인원 4명",
                "bed_room"         : "침실 1개",
                "bed"              : "침대 1개",
                "bath_room"        : "욕실 1개",
                "tag_title"        : [ "청결 강화, 훌륭한 숙소 위치, 11월 26일 4:00 PM까지 무료 취소 가능" ],
                "tag_detail"       : [ "최근 숙박한 게스트 중 90%가 위치에 별점 5점을 준 숙소입니다.,그 후에는 12월 1일 4:00 PM 전에 예약을 취소하면 첫 1박 요금 및 서비스 수수료를 제외한 요금의 50%가 환불됩니다." ],
                "description"      : "제주도에 놀러오세여여어어여어여여ㅓㅇ아야아이야이야이",
                "bedroom"          : [ "싱글 침대 2개, 슈퍼싱글 2개"],
                "bedtype"          : [ "1번 침실, 2번 침실" ],
                "latitude"         : "33.18481000",
                "longitude"        : "126.37482000",
                "rules_of_use"     : [ "체크인 시간: 오후 4:00 이후, 체크아웃 시간: 오후 12:00, 흡연 금지" ],
                "health_and_safety": [ "에어비앤비 청결 강화 기준을 준수합니다., 에어비앤비의 사회적 거리 두기 및 관련 가이드라인이 적용됩니다."],
                "refund_policy"    : [ "11월 26일 4:00 PM까지 무료 취소 가능" ],
                "host"             : True
            }
        ],
        'amenity_list': {
            'useable'  : [ '주방' ],
            'unuseable': [ '이용 불가: 일산화탄소 경보기' ]
        }
        })

    def test_room_get_not_found(self): 
        response = client.get('/rooms/4')
        
        self.assertEqual(response.status_code, 404)