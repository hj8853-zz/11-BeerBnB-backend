from django.urls import path

from .views import RoomReviewView, RoomReviewsView

urlpatterns = [
    path('',RoomReviewView.as_view()),
    path('/reviews/<int:id>',RoomReviewsView.as_view()),
    ]