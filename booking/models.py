from django.db import models

class Booking(models.Model): 
    check_in         = models.DateField()
    check_out        = models.DateField()
    price            = models.DecimalField(max_digits = 10, decimal_places = 2)
    cleaning_expense = models.DecimalField(max_digits = 10, decimal_places = 2)
    service_tax      = models.DecimalField(max_digits = 10, decimal_places = 2)
    accomodation_tax = models.DecimalField(max_digits = 10, decimal_places = 2)
    adult            = models.PositiveIntegerField()
    children         = models.PositiveIntegerField()
    infants          = models.PositiveIntegerField()
    user             = models.ForeignKey('user.User', on_delete = models.CASCADE)
    room             = models.ForeignKey('room.Room', on_delete = models.CASCADE)
    status           = models.ForeignKey('BookingStatus', on_delete = models.CASCADE)
    payment_method   = models.ForeignKey('PaymentMethod', on_delete = models.CASCADE)
    created_at       = models.DateTimeField(auto_now_add = True)

    class Meta: 
        db_table = 'bookings'

class BookingStatus(models.Model): 
    status = models.CharField(max_length = 128)

    class Meta: 
        db_table = 'booking_status'

class PaymentMethod(models.Model): 
    name = models.CharField(max_length = 128)

    class Meta: 
        db_table = 'payment_methods'