from django.db import models

from booking.models import Booking

class Review(models.Model):
    booking             = models.ForeignKey(Booking, on_delete = models.CASCADE, default = None)
    content             = models.TextField()
    cleanliness_score   = models.DecimalField(max_digits = 2, decimal_places = 1)
    communication_score = models.DecimalField(max_digits = 2, decimal_places = 1)
    check_in_score      = models.DecimalField(max_digits = 2, decimal_places = 1)
    accuracy_score      = models.DecimalField(max_digits = 2, decimal_places = 1)
    location_score      = models.DecimalField(max_digits = 2, decimal_places = 1)
    satisfaction_score  = models.DecimalField(max_digits = 2, decimal_places = 1)
    created_at          = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = "reviews"