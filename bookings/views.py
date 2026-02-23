from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer
from workers.models import Worker
from django.db import transaction
from datetime import datetime
from workers.models import WorkerAvailability

# CREATE BOOKING
class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 🔐 Role Check
        if request.user.user_type != "customer":
            return Response(
                {"error": "Only customers can create bookings"},
                status=status.HTTP_403_FORBIDDEN
            )

        worker_id = request.data.get("worker_id")
        service_address = request.data.get("service_address")
        booking_date = request.data.get("booking_date")
        booking_time = request.data.get("booking_time")

        # 🧾 Required Fields Validation
        if not all([worker_id, service_address, booking_date, booking_time]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        worker = get_object_or_404(Worker, id=worker_id)

        # 🗓 Parse Date & Time Safely
        try:
            booking_date_obj = datetime.strptime(booking_date, "%Y-%m-%d").date()
            booking_time_obj = datetime.strptime(booking_time, "%H:%M:%S").time()
        except ValueError:
            return Response(
                {"error": "Invalid date or time format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 📅 Check Worker Weekly Availability
        day_of_week = booking_date_obj.weekday()

        is_available = WorkerAvailability.objects.filter(
            worker=worker,
            day_of_week=day_of_week,
            start_time__lte=booking_time_obj,
            end_time__gte=booking_time_obj
        ).exists()

        if not is_available:
            return Response(
                {"error": "Worker not available at this time"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🚫 Prevent Double Booking
        existing_booking = Booking.objects.filter(
            worker=worker,
            booking_date=booking_date_obj,
            booking_time=booking_time_obj,
            status__in=["pending", "accepted"]
        ).exists()

        if existing_booking:
            return Response(
                {"error": "Worker already booked for this time slot"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 💾 Create Booking Safely
        with transaction.atomic():
            booking = Booking.objects.create(
                customer=request.user,
                worker=worker,
                service_address=service_address,
                booking_date=booking_date_obj,
                booking_time=booking_time_obj,
                status="pending",
            )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# UPDATE BOOKING STATUS (WORKER ONLY)
class UpdateBookingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        # 🔐 Role Check
        if request.user.user_type != "worker":
            return Response(
                {"error": "Only workers can update booking status"},
                status=status.HTTP_403_FORBIDDEN
            )

        booking = get_object_or_404(Booking, id=pk)

        new_status = request.data.get('status')

        if new_status not in ['accepted', 'completed', 'cancelled']:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.worker.user != request.user:
            return Response(
                {'error': 'You are not assigned to this booking'},
                status=status.HTTP_403_FORBIDDEN
            )

        booking.status = new_status
        booking.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data)


# CLIENT DASHBOARD
class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            customer=request.user
        ).order_by('-created_at')

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


# WORKER DASHBOARD
class WorkerBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(
            worker__user=request.user
        ).order_by('-created_at')

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
