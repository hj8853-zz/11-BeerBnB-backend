from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('rooms', include('room.urls')),
    path('booking', include('booking.urls')),
    path('review', include('review.urls'))
]