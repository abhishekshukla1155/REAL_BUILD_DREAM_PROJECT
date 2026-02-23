from django.urls import path
from .views import CreateReviewView

urlpatterns = [
    path('create/<int:booking_id>/', CreateReviewView.as_view(), name='create-review'),
]