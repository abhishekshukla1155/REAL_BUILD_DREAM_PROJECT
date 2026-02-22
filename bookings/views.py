from django.shortcuts import render
from google.protobuf.proto import serialize
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Booking
from .serializers import BookingSerializer
from workers.models import Worker

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.

class CreateBookingView(APIView):
    def post(self, request):

        worker_id = request.data.get('worker_id')
        service_address = request.data.get('service_address')

        if not worker_id or not service_address:
            return Response(
                {'error': 'worker_id and service_address cannot required'},
                status = status.HTTP_400_BAD_REQUEST
            )
        worker = get_object_or_404(Worker, id=worker_id)

        booking = Booking.objects.create(
            customer = request.user,
            worker = worker,
            service_address = service_address,
            status = 'pending',
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateBookingStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        booking = get_object_or_404(Booking, id=pk)

        new_status = request.data.get('status')

        if new_status not in ['accepted', 'completed', 'cancelled']:
            return Response(
                {'error': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.worker.user != request.user:
            return Response(
                {'error': 'You are not allowed to update this booking'},
                status=status.HTTP_403_FORBIDDEN
            )

        booking.status = new_status
        booking.save()

        serializer = BookingSerializer(booking)
        return Response(serializer.data)

class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class WorkerBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(workers_user=request.user).order_by('-created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)