from django.urls import path
from .views import CreateBookingView
from .views import UpdateBookingStatusView
from .views import MyBookingsView
from .views import WorkerBookingsView

urlpatterns = [
    path('create/', CreateBookingView.as_view(), name='create-booking'),
    path('<int:pk>/update-status/', UpdateBookingStatusView.as_view(), name='update-booking-status'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path("worker-bookings/", WorkerBookingsView.as_view(), name="worker-bookings"),

]