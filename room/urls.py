from django.urls import path

from .views import (
    RoomsView,
    RoomView
)

urlpatterns = [
    path('', RoomsView.as_view()),
    path('/<int:pk>', RoomView.as_view())
]