from django.db.models import Sum

from review.models import Review

def cal_review_avg(b_id, review, reviews):
    ls = Review.objects.filter(booking = b_id).aggregate(Sum(review))
    i_avg = list(ls)[1] / len(reviews)
    return i_avg