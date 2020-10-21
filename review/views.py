import json

from django.db.models import Q, Sum, Avg
from django.http      import JsonResponse
from django.views     import View

from room.models    import Room
from user.models    import User
from user.utils     import login_required
from .models        import Review
from booking.models import Booking

class RoomReviewView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(email = request.user.email)
            Review(
                booking             = Booking.objects.get(Q(user = user) & Q(room = data['room_id'])),
                content             = data['content'],
                cleanliness_score   = data['cleanliness_score'],
                communication_score = data['communication_score'],
                check_in_score      = data['check_in_score'],
                accuracy_score      = data['accuracy_score'],
                location_score      = data['location_score'],
                satisfaction_score  = data['satisfaction_score'],
            ).save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class RoomReviewsView(View):
    def get(self, request, id):
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 6))
        body = {
            "avg" : [],
            "list": []
        }
        try:
            room_id = Room.objects.filter(booking__room = id).first().id
            reviews = Review.objects.filter(booking__room = room_id)[offset:offset+limit]
            review_data = [
            {
                'user_name'    : review.booking.user.first_name,
                'user_profile' : [profile.profile_image for profile in review.booking.user.userprofile_set.all()],
                'created_at'   : review.created_at,
                'content'      : review.content
            }
            for review in reviews]

            reviews = Review.objects.filter(booking__room= room_id)
            cleanliness_score_avg = list(reviews.aggregate(Avg('cleanliness_score')).values())[0]
            communication_score_avg = list(reviews.aggregate(Avg('communication_score')).values())[0]
            check_in_score_avg = list(reviews.aggregate(Avg('check_in_score')).values())[0]
            accuracy_score_avg = list(reviews.aggregate(Avg('accuracy_score')).values())[0]
            location_score_avg = list(reviews.aggregate(Avg('location_score')).values())[0]
            satisfaction_score_avg = list(reviews.aggregate(Avg('satisfaction_score')).values())[0]
            rate_avg = (cleanliness_score_avg + communication_score_avg + check_in_score_avg + accuracy_score_avg + location_score_avg + satisfaction_score_avg) / 6
            avg = {
                "review"                  : reviews.count(),
                "rate_avg"                : round(rate_avg,1),
                "cleanliness_score_avg"   : round(cleanliness_score_avg,1),
                "communication_score_avg" : round(communication_score_avg,1),
                "check_in_score_avg"      : round(check_in_score_avg,1),
                "accuracy_score_avg"      : round(accuracy_score_avg,1),
                "location_score_avg"      : round(location_score_avg,1),
                "satisfaction_score_avg"  : round(satisfaction_score_avg,1)
            }
            body["avg"].append(avg)
            body["list"].append(review_data)
        except IndexError:
            pass
        return JsonResponse(body)