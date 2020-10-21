import json
import datetime

from django.views import View
from django.db import transaction, IntegrityError
from django.http import (
    JsonResponse,
    HttpResponse
)

from user.utils import login_required
from user.models import (
    User,
    UserProfile
)
from room.models import Room
from .models import (
    Booking,
    BookingStatus,
    PaymentMethod
)

class BookingView(View):
    @login_required
    def post(self, request):
        try: 
            data             = json.loads(request.body)
            user             = request.user
            room_id          = data['room_id']
            room             = Room.objects.get(id = room_id)
            price            = room.price
            check_in         = datetime.datetime.strptime(data['check_in'], '%Y-%m-%d')
            check_out        = datetime.datetime.strptime(data['check_out'], '%Y-%m-%d')
            adult            = data['adult']
            children         = data['children']
            infants          = data['infants']
            payment_method   = data['payment_method']
            total_price      = data['total_price']
            cleaning_expense = float(price) * 0.07
            service_tax      = float(price) * 0.06
            accomodation_tax = float(price) * 0.05

            with transaction.atomic():
                Booking.objects.create(
                    check_in         = check_in,
                    check_out        = check_out,
                    price            = total_price,
                    cleaning_expense = cleaning_expense,
                    service_tax      = service_tax,
                    accomodation_tax = accomodation_tax,
                    adult            = adult,
                    children         = children,
                    infants          = infants,
                    user             = user,
                    room             = room,
                    status           = BookingStatus.objects.get(status = '예약 대기'),
                    payment_method   = PaymentMethod.objects.get(name = payment_method),
                )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError: 
            return JsonResponse({'message' : 'INVALID_KEY'}, status=400)
        except IntegrityError: 
            return JsonResponse({'message' : 'TRANSACTION_FAILURE'}, status=400)
        except PaymentMethod.DoesNotExist: 
            return JsonResponse({'message' : 'DOES_NOT_EXIST_PAYMENT_METHOD'}, status = 400)
        except Room.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST_ROOM'}, status = 404)

    @login_required
    def patch(self, request):
        data = json.loads(request.body)
        try:
            user = request.user
            booking_room = Booking.objects.filter(user_id = request.user.id, room_id = data['room_id'], status_id = data['status_id'])
            if booking_room:
                Booking.objects.update(status_id = 2)
            return HttpResponse(status = 200)
                
        except KeyError:
            return JsonResponse({ 'message' : 'INVALID_KEYS' }, status = 400)