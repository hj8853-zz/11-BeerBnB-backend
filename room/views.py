import json
import sys

from django.views     import View
from django.db.models import Q
from django.http      import (
JsonResponse
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
    BedType,
    BedRoom
)

class RoomsView(View):
    def get(self, request):
        limit        = int(request.GET.get('limit', 10))
        offset       = int(request.GET.get('offset', 0))
        check_in     = request.GET.get('checkin', None)
        check_out    = request.GET.get('checkout', None)
        q_refund     = request.GET.get('refund', '')
        q_home_type  = request.GET.getlist('home_type', None)
        
        if q_refund and not q_home_type:
            rooms = Room.objects.filter(refundpolicy__refund_policy__contains = '무료 취소')
        elif q_home_type and not q_refund:
            if len(q_home_type) == 1:
                if 'entire_house' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '전체')
                    )[offset:limit+offset]
                elif 'private_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '개인실')
                    )[offset:limit+offset]
                elif 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '객실')
                    )[offset:limit+offset]
            elif len(q_home_type) == 2:
                if 'entire_house' in q_home_type and 'private_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '전체')
                        |Q(buildingtype__sub_title__contains = '개인실')
                    )[offset:limit+offset]
                elif 'entire_house' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '전체')
                        |Q(buildingtype__sub_title__contains = '객실')    
                    )[offset:limit+offset]
                elif 'private_room' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '개인실')
                        |Q(buildingtype__sub_title__contains = '객실')
                    )[offset:limit+offset]
            elif len(q_home_type) == 3:
                if 'entire_house' in q_home_type and 'private_room' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '전체')
                        |Q(buildingtype__sub_title__contains = '개인실')
                        |Q(buildingtype__sub_title__contains = '객실')
                    )[offset:limit+offset]
        elif q_home_type and q_refund:
            if len(q_home_type) == 1:
                if 'entire_house' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '전체')
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
                elif 'private_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '개인실')
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
                elif 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(buildingtype__sub_title__contains = '객실')
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
            elif len(q_home_type) == 2:
                if 'entire_house' in q_home_type and 'private_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(
                            Q(buildingtype__sub_title__contains = '전체')
                            |Q(buildingtype__sub_title__contains = '개인실')
                        )
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
                elif 'entire_house' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(
                            Q(buildingtype__sub_title__contains = '전체')
                            |Q(buildingtype__sub_title__contains = '객실')
                        )
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
                elif 'private_room' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(
                            Q(buildingtype__sub_title__contains = '개인실')
                            |Q(buildingtype__sub_title__contains = '객실')
                        )
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
            elif len(q_home_type) == 3:
                if 'entire_house' in q_home_type and 'private_room' in q_home_type and 'guest_room' in q_home_type:
                    rooms = Room.objects.filter(
                        Q(
                            Q(buildingtype__sub_title__contains = '전체')
                            |Q(buildingtype__sub_title__contains = '개인실')
                            |Q(buildingtype__sub_title__contains = '객실')
                        )
                        &Q(refundpolicy__refund_policy__contains = '무료 취소')
                    )[offset:limit+offset]
        else:
            rooms = Room.objects.select_related('host').prefetch_related('image_set', 'roomamenity_set')[offset:limit+offset]

        if rooms:
            count = rooms.count()
            room_data = [
                {
                    'id'           : room.id,
                    'image_url'    : [ image.image_url for image in room.image_set.all() ],
                    'address'      : room.address,
                    'title'        : room.title,
                    'max_personnal': room.max_personnal,
                    'bed_room'     : room.bed_room,
                    'bed'          : room.bed,
                    'bath_room'    : room.bath_room,
                    'amenity'      : [ amenities.amenity.name for amenities in room.roomamenity_set.all() ],
                    'price'        : room.price,
                    'latitude'     : room.latitude,
                    'longitude'    : room.longitude,
                    'host'         : room.host.is_super_host
                }
                for room in rooms ]
            
            return JsonResponse({"rooms_list" : room_data, "total" : count}, status = 200)
        return JsonResponse({'message' : 'NOT_FOUND'}, status = 404)

class RoomView(View):
    def get(self, request, pk):
        if Room.objects.filter(pk = pk):
            rooms = Room.objects.select_related('host').prefetch_related(
                'buildingtype_set',
                'image_set',
                'tag_set',
                'ruleuse_set',
                'healthsafety_set',
                'refundpolicy_set',
                'roomamenity_set',
                'bedtyperoom_set'
            ).filter(pk = pk)
            detail_list = [
                {
                    'id'               : room.id,
                    'address'          : room.address,
                    'image_url'        : [ image.image_url for image in room.image_set.all() ],
                    'title'            : room.title,
                    'sub_title'        : [ title.sub_title for title in room.buildingtype_set.all() ],
                    'max_personnal'    : room.max_personnal,
                    'bed_room'         : room.bed_room,
                    'bed'              : room.bed,
                    'bath_room'        : room.bath_room,
                    'tag_title'        : [ tag.title for tag in room.tag_set.all() ],
                    'tag_detail'       : [ tag.detail for tag in room.tag_set.all() ],
                    'description'      : room.description,
                    'bedroom'          : [ bedrooms.bedroom.name for bedrooms in room.bedtyperoom_set.all() ],
                    'bedtype'          : [ bedtypes.bedtype.name for bedtypes in room.bedtyperoom_set.all() ],
                    'latitude'         : room.latitude,
                    'longitude'        : room.longitude,
                    'rules_of_use'     : [ rules_of_uses.rules_of_use for rules_of_uses in room.ruleuse_set.all() ],
                    'health_and_safety': [ health_and_safeties.health_and_safety for health_and_safeties in room.healthsafety_set.all() ],
                    'refund_policy'    : [ refund_policies.refund_policy for refund_policies in room.refundpolicy_set.all() ],
                    'host'             : room.host.is_super_host
                } 
                for room in rooms ]
            useable = []
            unuseable = []
            for room in rooms:
                for amenities in room.roomamenity_set.all():
                    if "경보기" in amenities.amenity.name:
                        unuseable.append(amenities.amenity.name)
                    else:    
                        useable.append(amenities.amenity.name)
            amenity_list = {
                    'useable' : useable,
                    'unuseable' : unuseable
                }
            return JsonResponse({'detail_list' : detail_list, 'amenity_list' : amenity_list}, status = 200)
        return JsonResponse({'message' : 'DOES NOT EXIST ROOM'}, status = 404)